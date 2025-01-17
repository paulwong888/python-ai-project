import torch, threading
from a00_constant import LLAMA3_LAW_PATH
from threading import Thread
from transformers import AutoTokenizer, LlamaForCausalLM, GenerationConfig, TextIteratorStreamer

device = "cuda" if torch.cuda.is_available() else "cpu"

class LawLlama3Runner():

    def __init__(self):
        model_path = LLAMA3_LAW_PATH
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = LlamaForCausalLM.from_pretrained(
            model_path,
            device_map="auto", load_in_8bit=True
        )

    def generate(self, instruction):
        if not instruction:
            return
        prompt = instruction.strip()

        batch = self.tokenizer(prompt, return_tensors="pt", add_special_tokens=True)

        lock = threading.Lock()
        self.model.eval()
        with lock:
            with torch.torch.no_grad():
                generation_config = GenerationConfig(
                    repetition_penalty=1.1,
                    max_new_tokens=1024,
                    temperature=0.9,
                    top_p=0.95,
                    top_k=40,
                    bos_token_id=self.tokenizer.bos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.pad_token_id,
                    do_sample=True,
                    use_cache=True,
                    return_dict_in_generate=True,
                    output_attentions=False,
                    output_hidden_states=False,
                    output_scores=False,
                )
                streamer = TextIteratorStreamer(self.tokenizer)
                generation_kwargs = {
                    "inputs": batch["input_ids"].to(device),
                    "attention_mask": batch["attention_mask"].to(device),
                    "generation_config": generation_config,
                    "streamer": streamer,
                }

                thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
                thread.start()
                # self.model.generate(kwargs=generation_kwargs)

                all_text = ""

                for new_text in streamer:
                    all_text += new_text
                    yield all_text

if __name__ == "__main__":
    llama3_runner = LawLlama3Runner()
    # print(llama3_runner.predict("请介绍下香港演员周星驰的主要作品"))
    message = """
      甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
      当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
      这种情况下，仲裁协议是否有效?
      """
    for text in llama3_runner.generate(message):
        print(text, end="")