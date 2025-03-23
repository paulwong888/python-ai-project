import torch
from a00_constant import *
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer

class MyDataset():
    def __init__(self):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.EOS_TOKEN = tokenizer.eos_token
        device = "cuda" if torch.cuda.is_available() else "cpu"
        train_dataset = load_dataset(dataset_dir, split="train")
        test_dataset = load_dataset(dataset_dir, split="test")

        self.train_dataset = self.pre_processing(train_dataset)
        self.test_dataset = self.pre_processing(test_dataset)
        # self.train_dataset = self.train_dataset.rename_columns({"instruction": "prompt", "output": "completion"})
        # self.test_dataset = self.test_dataset.rename_columns({"instruction": "prompt", "output": "completion"})

    def format_input(self, samples):
        instructions = samples["instruction"]
        outputs = samples["output"]
        texts = []
        for instruction, output in zip(instructions, outputs):
            text = prompt_style.format(instruction, output) + self.EOS_TOKEN
            texts.append(text)
        return {"text": texts}

    def pre_processing(self, dataset: Dataset):
        return dataset.map(
            lambda x: self.format_input(x),
            batched = True,
            remove_columns = ["instruction", "input", "output"],
        )

if __name__ == "__main__":
    my_dataset = MyDataset()
    print(my_dataset.train_dataset)
    print(my_dataset.test_dataset)
    print(my_dataset.train_dataset[0])