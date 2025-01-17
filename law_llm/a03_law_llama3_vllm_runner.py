from a00_constant import LLAMA3_LAW_PATH
from vllm import LLM, SamplingParams

class LawLlama3VllmRunner():
    def __init__(self):
        self.model = self.load_model()
        self.tokenizer = self.model.get_tokenizer()
        self.sampling_params = self.build_sampling_params(self.model)

    def load_model(self):
        model_path = LLAMA3_LAW_PATH
        return LLM(
            model_path, 
            quantization="bitsandbytes", 
            load_format="bitsandbytes",
            max_model_len=1024,
        )

    def build_sampling_params(self, model: LLM):
        sampling_params = model.get_default_sampling_params()
        sampling_params.temperature = 0.1
        sampling_params.seed = 42
        sampling_params.max_tokens = 256
        return sampling_params

    def predict(self, message):
        # input = self.tokenizer(message, return_tensors="pt", add_special_tokens=True)
        output = self.model.generate(message, self.sampling_params)
        return output

if __name__ == "__main__":
    law_llama3_vllm = LawLlama3VllmRunner()
    message = """
      甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
      当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
      这种情况下，仲裁协议是否有效?
    """
    generated_text = law_llama3_vllm.predict(message)
    # print([0].outputs[0].text)
    print(f"Generated text: {generated_text[0].outputs[0].text!r}")
