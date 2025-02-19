from a00_constant import *
from unsloth import FastLanguageModel
from transformers import LlamaTokenizerFast, LlamaForCausalLM

class MyModel:
    def __init__(self):
        # self.tokenizer: LlamaTokenizerFast
        # self.model: LlamaForCausalLM
            # dtype=torch.float16,
            # device_map="auto",
            # dtype=None,
            # torch_dtype=torch.float16,
        super(MyModel, self).__init__()
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=2048,
            load_in_4bit=True,
        )
        # self.model = self.model.to(device)

    def get_peft_model(self):
        return FastLanguageModel.get_peft_model(
            model=self.model,
            use_gradient_checkpointing="unsloth",  # True or "unsloth" for very long context
        )

    def generate(self,question):
        FastLanguageModel.for_inference(self.model)
        input = self.tokenizer([prompt_style.format(question, "")], return_tensors="pt").to(device)
        output = self.model.generate(
            input_ids = input.input_ids,
            attention_mask = input.attention_mask,
            max_new_tokens = 1200,
            use_cache = True
        )
        response = self.tokenizer.batch_decode(output)
        print(response[0].split("### Response:")[1])
        return response
    
if __name__ == "__main__":
    my_model = MyModel()
    print(type(my_model))
    question = "A 61-year-old woman with a long history of involuntary urine loss during activities like coughing or sneezing but no leakage at night undergoes a gynecological exam and Q-tip test. Based on these findings, what would cystometry most likely reveal about her residual volume and detrusor contractions?"
    my_model.generate(question)