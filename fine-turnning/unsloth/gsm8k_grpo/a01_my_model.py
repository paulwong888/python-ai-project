from a00_constant import *
from unsloth import FastLanguageModel

class MyModel():
    def __init__(self):
        my_model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name = model_name,
            max_seq_length = max_seq_length,
            load_in_4bit = load_in_4bit,
            fast_inference = fast_inference,
            max_lora_rank = max_lora_rank,
            gpu_memory_utilization = gpu_memory_utilization
        )
        self.peft_my_model = FastLanguageModel.get_peft_model(
            model = my_model,
            r = max_lora_rank,
            lora_alpha = max_lora_rank,
            use_gradient_checkpointing = use_gradient_checkpointing,
            random_state = random_state
        )

if __name__ == "__main__":
    my_model = MyModel()