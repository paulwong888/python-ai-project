from a00_constant import *
from a01_test_message import *
from vllm import LLM, SamplingParams

class VllmRunner():
    def __init__(self):
        self.model = self.load_model()
        self.tokenizer = self.model.get_tokenizer()
        self.sampling_params = self.build_sampling_params(self.model)

    def load_model(self):
        model_path = GEMMA_3_12B_IT_PATH
        return LLM(
            model_path, 
            quantization="bitsandbytes", 
            load_format="bitsandbytes",
            # quantization="gguf", #should provide a gguf file
            # load_format="gguf",  #should provide a gguf file
            max_model_len=1024,
            dtype="half",
            gpu_memory_utilization=0.90,
            enforce_eager=True,
            # tensor_parallel_size=2,
        )

    def build_sampling_params(self, model: LLM):
        sampling_params = model.get_default_sampling_params()
        sampling_params.temperature = 0.1
        sampling_params.seed = 42
        sampling_params.max_tokens = 256
        return sampling_params

    def predict(self, message):
        # input = self.tokenizer(message, return_tensors="pt", add_special_tokens=True)
        # output = self.model.generate(message, self.sampling_params)
        output = self.model.generate([message])
        return output

if __name__ == "__main__":
    law_llama3_vllm = VllmRunner()
    generated_text = law_llama3_vllm.predict(json_output_message)
    # print([0].outputs[0].text)
    for item in generated_text:
        print(item)
    print(generated_text[0])
    print(f"Generated text: {generated_text[0].outputs[0].text}")
