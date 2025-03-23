import torch
from a00_constant import *
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer
from trl import DataCollatorForCompletionOnlyLM

class MyDataset():
    def __init__(self):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.EOS_TOKEN = tokenizer.eos_token
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.train_dataset = load_dataset(dataset_dir, split="train")
        self.test_dataset = load_dataset(dataset_dir, split="test")

        self.train_dataset = self.train_dataset.rename_columns({"instruction": "prompt", "output": "completion"})
        self.test_dataset = self.test_dataset.rename_columns({"instruction": "prompt", "output": "completion"})
        # self.train_dataset = self.pre_processing(train_dataset)
        # self.test_dataset = self.pre_processing(test_dataset)
        print(self.EOS_TOKEN)
        self.data_collator = DataCollatorForCompletionOnlyLM(response_template, tokenizer=tokenizer)

    def format_prompt(self, sample):
        # print(type(sample))
        instruction = sample["instruction"]
        input = sample["input"]
        output = sample["output"]
        text = prompt_style.format(instruction, output) + self.EOS_TOKEN
        # return {"text": text}
        return text

    def format_prompt_all(self, samples):
        print(type(samples))
        result = []
        instructions = samples["instruction"]
        inputs = samples["input"]
        outputs = samples["output"]
        for instruction, input, output in zip(instructions, inputs, outputs):
            text = prompt_style.format(instruction, output) + self.EOS_TOKEN
            result.append(text)
        return result

    def pre_processing(self, dataset: Dataset):
        print(type(dataset))
        return dataset.map(
            lambda x: self.format_prompt(x),
            # batched = True, # 一次传入全部数据
            remove_columns = ["instruction", "input", "output"]
        )

if __name__ == "__main__":
    my_dataset = MyDataset()
    print(my_dataset.train_dataset)
    print(my_dataset.test_dataset)
    print(my_dataset.train_dataset[0])