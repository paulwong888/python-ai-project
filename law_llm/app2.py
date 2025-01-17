import json, requests
import gradio as gr
from a00_constant import LLAMA3_LAW_VLLM_ID
from a04_vllm_client import VllmClient
from openai import OpenAI

# 模拟的大模型推理函数
def mock_large_model_inference(input_text):
    # 这里模拟一个逐字输出的过程
    output_text = ""
    for char in input_text:
        output_text += char
        yield output_text  # 逐字返回结果

def http_bot(prompt):
    headers = {"User-Agent": "vLLM Client", "Content-Type": "application/json"}
    pload = {
        "model": LLAMA3_LAW_VLLM_ID,
        "prompt": prompt,
        "stream": True,
        "max_tokens": 128,
    }
    response = requests.post("http://192.168.0.106:8080/v1/completions",
                             headers=headers,
                             json=pload,
                             stream=True)

    for chunk in response.iter_lines(chunk_size=8192,
                                     decode_unicode=False,
                                     delimiter=b"\0"):
        if chunk:
            print(type(chunk))
            data = json.loads(chunk.decode("utf-8"))
            output = data["text"][0]
            yield output


# 创建 Gradio 界面
with gr.Blocks() as demo:
    message = """甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
        当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
        这种情况下，仲裁协议是否有效?
    """
    vllm_client = VllmClient()
    iface = gr.Interface(
        fn=vllm_client.completions,
        inputs=gr.Textbox(lines=2, placeholder="请输入您的法律问题", value=message.strip()),
        outputs=gr.Textbox(lines=2, placeholder="答案将逐字显示在这里..."),
        title="法律咨询 - Present By Paul",
        description="请在下方输入您的法律问题，然后点击提交。"
    )

# 启动 Gradio 界面
demo.queue(max_size=5, default_concurrency_limit=3).launch(server_name="0.0.0.0")