import sounddevice as sd
import numpy as np
import requests
import base64
import json
import wave
import io
import time
import asyncio
import aiohttp
import uuid
import queue
import threading
from typing import Optional, List
import soundfile as sf

class VoiceClient:
    def __init__(self, server_url: str = "http://localhost:32550"):
        # 基础配置
        self.server_url = server_url
        self.sample_rate = 16000
        self.channels = 1
        self.chunk_size = 1024  # 增大chunk size
        self.dtype = np.int16  # 明确指定数据类型
        self.is_recording = False
        self.uid = str(uuid.uuid4())
        
        # 音频处理相关
        self.audio_chunks: List[np.ndarray] = []
        self.audio_queue = queue.Queue()  # 改回同步队列
        self.send_queue = asyncio.Queue()   # 用于发送到服务器的队列
        
        # 状态控制
        self.is_playing = False
        self.stop = False
        
        # 添加音频播放配置
        self.output_sample_rate = 24000  # 服务器返回的音频采样率
        self.output_device = None  # 输出设备
        self.playing_audio = False
        
        # 音频播放相关
        self.playing = False
        self.audio_chunks = []
        self.all_voice = []  # 存储所有音频片段
        
        self.loop = None  # 保存事件循环引用
        
        self.conversation_started = False  # 添加对话状态标记
        
    def _generate_uid(self) -> str:
        return str(uuid.uuid4())

    async def initialize_conversation(self):
        """初始化对话"""
        url = f"{self.server_url}/api/v1/completions"
        
        init_message = {
            "messages": [{
                "role": "user",
                "content": [{"type": "none"}]
            }],
            "stream": True
        }

        headers = {
            "Content-Type": "application/json",
            "service": "minicpmo-server",
            "uid": self.uid
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=init_message, headers=headers) as response:
                    if response.status == 200:
                        print("Conversation initialized successfully")
                        self.conversation_started = True
                    else:
                        print(f"Failed to initialize conversation: {response.status}")
            except Exception as e:
                print(f"Error initializing conversation: {e}")

    async def initialize_sse(self):
        """初始化SSE连接"""
        url = f"{self.server_url}/api/v1/completions"  # 使用 completions
        
        init_message = {
            "messages": [{
                "role": "user",
                "content": [{"type": "none"}]
            }],
            "stream": True
        }

        headers = {
            "Content-Type": "application/json",
            "service": "minicpmo-server",
            "uid": self.uid
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url,
                    json=init_message,
                    headers=headers,
                    chunked=False
                ) as response:
                    buffer = ""
                    # 使用 content.iter_any() 替代 iter_lines
                    async for chunk in response.content.iter_any():
                        if chunk:
                            text = chunk.decode('utf-8')
                            buffer += text
                            
                            # 处理SSE消息
                            while '\n\n' in buffer:
                                message, buffer = buffer.split('\n\n', 1)
                                if message.startswith('data: '):
                                    try:
                                        data = json.loads(message[6:])
                                        await self._handle_sse_message(data)
                                    except json.JSONDecodeError:
                                        print(f"Failed to decode SSE message: {message}")
                                    except Exception as e:
                                        print(f"Error processing SSE message: {e}")
            except Exception as e:
                print(f"SSE connection error: {e}")
                raise

    async def _handle_sse_message(self, data):
        """处理SSE消息"""
        try:
            if "choices" in data and data["choices"]:
                choice = data["choices"][0]
                
                # 处理文本
                if "text" in choice:
                    text = choice["text"].replace("<end>", "")
                    print(f"Received text: {text}")
                
                # 处理音频
                if "audio" in choice:
                    print("Received audio response")
                    audio_data = choice["audio"]
                    if audio_data:
                        # 将音频数据加入队列
                        self.audio_queue.put(audio_data)
                        self.all_voice.append(audio_data)
                        
                        # 如果没有在播放，开始播放
                        if not self.playing:
                            asyncio.create_task(self.play_audio_queue())
                        
        except Exception as e:
            print(f"Error handling SSE message: {e}")

    async def play_audio_queue(self):
        """播放音频队列"""
        self.playing = True
        try:
            while True:
                # 获取音频数据
                try:
                    audio_data = self.audio_queue.get(timeout=1.0)
                except queue.Empty:
                    if self.audio_queue.empty():
                        break
                    continue

                try:
                    # 解码并播放音频
                    with io.BytesIO(audio_data) as audio_io:
                        audio_data, sample_rate = sf.read(audio_io)
                        
                        # 确保音频数据是float32类型
                        if audio_data.dtype != np.float32:
                            audio_data = audio_data.astype(np.float32)
                        
                        # 非阻塞播放
                        sd.play(audio_data, sample_rate)
                        # 等待一小段时间确保播放开始
                        await asyncio.sleep(0.1)
                        
                except Exception as e:
                    print(f"Error playing audio chunk: {e}")
                    continue
                
        finally:
            self.playing = False
	
    def print_audio_devices(self):
        """打印音频设备信息"""
        print("\nAvailable audio devices:")
        print(sd.query_devices())

    def audio_callback(self, indata, frames, time, status):
        """音频回调函数,处理录音数据"""
        if status:
            print(f"Status: {status}")
            
        if self.is_recording:
            # 转换音频格式
            audio_chunk = (indata * 32767).astype(np.int16)
            self.audio_chunks.append(audio_chunk)
            
            # 检查是否收集到1秒的数据
            total_samples = sum(len(chunk) for chunk in self.audio_chunks)
            if total_samples >= self.sample_rate:
                # 合并音频数据
                merged_audio = np.concatenate(self.audio_chunks)
                one_second_audio = merged_audio[:self.sample_rate]
                
                # 将多余的数据保留
                excess_samples = merged_audio[self.sample_rate:]
                self.audio_chunks = [excess_samples] if len(excess_samples) > 0 else []
                
                # 使用普通队列
                self.audio_queue.put(one_second_audio)

    async def process_audio_queue(self):
        """处理音频发送队列"""
        while self.is_recording:
            try:
                # 非阻塞方式获取音频数据
                try:
                    audio_data = self.audio_queue.get_nowait()
                    await self.send_audio_chunk(audio_data)
                except queue.Empty:
                    await asyncio.sleep(0.1)
                    continue
            except Exception as e:
                print(f"Error processing audio: {e}")
            await asyncio.sleep(0.01)

    def encode_audio(self, audio_data: np.ndarray) -> str:
        """将numpy数组编码为WAV格式的base64字符串"""
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, 'wb') as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(2)  # 16-bit audio
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            return base64.b64encode(wav_io.getvalue()).decode('utf-8')

    async def send_audio_chunk(self, audio_data: np.ndarray):
        """发送音频数据到服务器"""
        # 确保对话已初始化
        if not self.conversation_started:
            print("Waiting for conversation to initialize...")
            return

        try:
            base64_audio = self.encode_audio(audio_data)
            
            message = {
                "messages": [{
                    "role": "user",
                    "content": [{
                        "type": "input_audio",
                        "input_audio": {
                            "data": base64_audio,
                            "format": "wav",
                            "timestamp": str(int(time.time() * 1000))
                        }
                    }]
                }],
                "stream": True
            }

            url = f"{self.server_url}/api/v1/stream"
            headers = {
                "Content-Type": "application/json",
                "service": "minicpmo-server",
                "uid": self.uid
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=message, headers=headers) as response:
                    if response.status != 200:
                        print(f"Error sending audio: {response.status}")
                        response_text = await response.text()
                        print(f"Response: {response_text}")
                        return
                    print("Audio chunk sent successfully")
                    
                    # 读取响应
                    async for chunk in response.content.iter_any():
                        if chunk:
                            text = chunk.decode('utf-8')
                            if text.startswith('data: '):
                                try:
                                    data = json.loads(text[6:])
                                    await self._handle_sse_message(data)
                                except json.JSONDecodeError:
                                    print(f"Failed to decode response: {text}")
                                except Exception as e:
                                    print(f"Error processing response: {e}")
        except Exception as e:
            print(f"Error sending audio: {e}")

    def start_recording(self):
        """开始录音"""
        self.is_recording = True
        self.audio_chunks = []
        
        # 修改录音流配置
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self.audio_callback,
            dtype=np.float32,  # sounddevice使用float32
            blocksize=self.chunk_size,
            device=None  # 使用默认设备
        ):
            print("Recording started...")
            try:
                while self.is_recording:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.stop_recording()

    def stop_recording(self):
        """停止录音"""
        self.is_recording = False
        print("Recording stopped.")

async def main():
    # 修改健康检查的URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:32550/health") as response:
                if response.status != 200:
                    print("Server is not ready")
                    return
    except Exception as e:
        print(f"Cannot connect to server: {e}")
        print("Please make sure the server is running on http://localhost:32550")
        return

    # 创建客户端实例，使用基础URL
    client = VoiceClient("http://localhost:32550")
    client.print_audio_devices()
    
    try:
        # 首先初始化对话
        await client.initialize_conversation()
        
        if not client.conversation_started:
            print("Failed to initialize conversation")
            return
            
        # 创建录音线程
        record_thread = threading.Thread(target=client.start_recording)
        record_thread.start()
        
        # 创建音频处理任务
        audio_task = asyncio.create_task(client.process_audio_queue())
        
        # 等待任务完成
        await audio_task
        
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        client.stop_recording()
        if record_thread.is_alive():
            record_thread.join()

if __name__ == "__main__":
    try:
        # 检查服务器是否运行
        print("Checking server status...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Program terminated with error: {e}")
