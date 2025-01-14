import torch
from a00_constant import LLAMA3_LAW_PATH, QWEN_REPO_ID
from transformers import LlamaForCausalLM, AutoTokenizer, AutoModelForCausalLM

class Llama3Runner():
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # model_name = QWEN_REPO_ID
        model_name = LLAMA3_LAW_PATH
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, device_map="auto", 
            # load_in_4bit=True,
            load_in_8bit=True,
        )

    def predict(self, message: str):
        # {"role": "system", "content": "You are a helpful assistant system."},
        mesage = [
            {"role": "system", "content": "You are an assistant who provides precise and direct answers."},
            {"role": "user", "content": message},
        ]
        message = self.tokenizer.apply_chat_template(
            mesage, tokenize=False, add_generation_prompt=True
        )
        input = self.tokenizer([message], return_tensors="pt").to(self.device)

        # model_input = self.tokenizer(message, return_tensors="pt").to(self.device)

        output = self.model.generate(**input, max_new_tokens=512)
        # output = self.model.generate(**model_input)
        response = self.tokenizer.batch_decode(output, skip_special_tokens=True)
        return response
    
if __name__ == "__main__":
    llama3_runner = Llama3Runner()
    # print(llama3_runner.predict("请介绍下香港演员周星驰的主要作品"))
    message = """
      甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
      当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
      这种情况下，仲裁协议是否有效?
      """
    print(llama3_runner.predict(message))
    