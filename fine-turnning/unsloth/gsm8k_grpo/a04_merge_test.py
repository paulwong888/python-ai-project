from a00_constant import *
from a01_my_model import MyModel
from unsloth import FastLanguageModel
from transformers import LlamaForCausalLM, PreTrainedTokenizer
from vllm import SamplingParams

"""
{
  "answer": [
    "# 18",
    "# 3"
  ],
  "prompt": [
    [
      {
        "content": "\nRespond in the following format:\n<reasoning>\n...\n</reasoning>\n<answer>\n...\n</answer>\n",
        "role": "system"
      },
      {
        "content": "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?",
        "role": "user"
      }
    ],
    [
      {
        "content": "\nRespond in the following format:\n<reasoning>\n...\n</reasoning>\n<answer>\n...\n</answer>\n",
        "role": "system"
      },
      {
        "content": "A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?",
        "role": "user"
      }
    ]
  ]
}
"""
class MyMerge():
    def __init__(self):
        # self.my_model, self.tokenizer = FastLanguageModel.from_pretrained(
        #     model_name, fast_inference=fast_inference,
        #     gpu_memory_utilization=0.98, max_seq_length=max_seq_length,
        #     load_in_4bit=True
        # )
        temp_model = MyModel()
        self.my_model = temp_model.ll_model
        self.peft_my_model = temp_model.peft_my_model
        self.tokenizer = temp_model.tokenizer
        
        self.peft_my_model.load_adapter(adapter_path, "adapter_name1")


if __name__ == "__main__":
    my_merge = MyMerge()
    # my_model = my_merge.my_model
    my_model = my_merge.peft_my_model
    tokenizer: PreTrainedTokenizer = my_merge.tokenizer
    # question = "A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?"
    question = "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?"
    input = tokenizer.apply_chat_template(
        conversation = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
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
    output = my_model.fast_generate(
        [input],
        sampling_params = sampling_params,
        # lora_request = my_model.load_adapter(adapter_path)
        # lora_request = None
    )
    print(output[0].outputs[0].text)
