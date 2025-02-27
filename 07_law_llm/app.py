import gradio as gr
import time
from a02_law_llama3_runner import LawLlama3Runner

def gen_response(message: str, progress=gr.Progress()):
    time.sleep(6)  # 继续模拟处理时间
    return "Hello World!"

if __name__ == "__main__":
    law_llam3_runner = LawLlama3Runner()
    with gr.Blocks() as demo:
        iface = gr.Interface(
            fn=law_llam3_runner.generate,
            inputs=gr.Textbox(lines=2, placeholder="请输入您的法律问题"),
            outputs=gr.Textbox(lines=2),
            title="法律咨询 - Present By Paul",
            description="请在下方输入您的法律问题，然后点击提交。"
        )

    demo.queue(max_size=5, default_concurrency_limit=2).launch(server_name="0.0.0.0")