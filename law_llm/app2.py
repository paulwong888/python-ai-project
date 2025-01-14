import gradio as gr

# 模拟的大模型推理函数
def mock_large_model_inference(input_text):
    # 这里模拟一个逐字输出的过程
    output_text = ""
    for char in input_text:
        output_text += char
        yield output_text  # 逐字返回结果


# 创建 Gradio 界面
with gr.Blocks() as demo:
    with gr.Row():
        input_text = gr.Textbox(placeholder="请输入您的法律咨询问题...", lines=2)
        submit_btn = gr.Button("Submit")
    
    output_text = gr.Textbox(placeholder="答案将逐字显示在这里...", interactive=True)
    
    submit_btn.click(
        mock_large_model_inference,
        inputs=input_text,
        outputs=output_text
    )

# 启动 Gradio 界面
demo.launch(server_name="0.0.0.0")