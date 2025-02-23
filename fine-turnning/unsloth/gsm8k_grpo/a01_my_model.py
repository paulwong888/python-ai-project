from a00_constant import *
from unsloth import FastLanguageModel
from vllm import SamplingParams
from transformers import PreTrainedTokenizer

class MyModel():
    def __init__(self):
        self.tokenizer: PreTrainedTokenizer
        self.ll_model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name = model_name,
            max_seq_length = max_seq_length,
            load_in_4bit = load_in_4bit,
            fast_inference = fast_inference,
            max_lora_rank = max_lora_rank,
            gpu_memory_utilization = gpu_memory_utilization
        )
        self.peft_my_model = FastLanguageModel.get_peft_model(
            model = self.ll_model,
            r = max_lora_rank,
            lora_alpha = max_lora_rank,
            use_gradient_checkpointing = use_gradient_checkpointing,
            random_state = random_state
        )
        # self.peft_my_model.load_adapter(adapter_path, "adapter_name1")

    def fast_generate(self, question: str):
        input = self.tokenizer.apply_chat_template(
        conversation = [
            # {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        tokenize = False, 
        add_generation_prompt = True
    )
        print(type(input))
        sampling_params = SamplingParams(
            temperature = 0.8,
            top_p = 0.95,
            max_tokens = 1024
        )
        output = self.ll_model.fast_generate(
            input,
            sampling_params = sampling_params
        )
        print(output[0].outputs[0].text)

if __name__ == "__main__":
    my_model = MyModel()
    question = "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?"
    my_model.fast_generate(question)
