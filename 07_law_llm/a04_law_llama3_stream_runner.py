import asyncio, uuid
from a00_constant import LLAMA3_LAW_PATH
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from transformers import AutoTokenizer

class LawLlama3VllmStreamRunner():
    def __init__(self):
        self.model_path = LLAMA3_LAW_PATH
        self.model = self.build_asyncio_engine()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.sampling_params = self.build_sampling_params()

    def build_asyncio_engine(self):
        engine_args = AsyncEngineArgs(
            model= self.model_path,
            quantization="bitsandbytes",
            load_format="bitsandbytes",
            max_model_len=2048,
        )
        return AsyncLLMEngine.from_engine_args(engine_args)
    
    def build_sampling_params(self):
        return SamplingParams(
            temperature=0.2,
            top_p=0.95,
            seed=42,
            stop_token_ids=[self.tokenizer.eos_token_id] + 
                self.tokenizer.additional_special_tokens_ids,
            skip_special_tokens=True,
        )
    
    async def predict(self, message: str):
        request_id = "chatcmpl-{}".format(uuid.uuid4().hex)
        outputs = self.model.generate(message, self.sampling_params, request_id)
        async for output in outputs:
            text = output.outputs[0].text
            print(text, end="", flush=True)

if __name__ == "__main__":
    law_llama3_vllm_ruuner = LawLlama3VllmStreamRunner()
    message = """
      甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
      当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
      这种情况下，仲裁协议是否有效?
    """
    asyncio.run(law_llama3_vllm_ruuner.predict(message))