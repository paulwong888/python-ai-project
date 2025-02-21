from a00_constant import *
from datasets import load_dataset
from transformers import Qwen2Tokenizer

class MyDataset:
    def __init__(self):
        self.tokenizer: Qwen2Tokenizer = Qwen2Tokenizer.from_pretrained(model_name)
        self.EOS_TOKEN = self.tokenizer.eos_token
        dataset = load_dataset(
            "json", "train",
            data_dir=dataset_dir
        )
        self.train_dataset = dataset["train"]
        self.test_dataset = dataset["test"]
        self.train_dataset = self.pre_process_dataset(self.train_dataset)
        self.test_dataset = self.pre_process_dataset(self.test_dataset)

    def pre_process_dataset(self, dataset):
        return dataset.map(
            lambda x: self.format_prompt(x),
            remoove_columns = ["instruction", "input", "output"],
            batched = True,
        )

    def format_prompt(self, samples):
        instructions = samples["instruction"]
        inputs = samples["input"]
        outputs = samples["output"]
        texts = []
        for instruction, input, output in zip(instructions, inputs, outputs):
            text = prompt_style.format(instruction+input, output) + self.EOS_TOKEN
            texts.append(text)
        return {"text": texts}
0
if __name__ == "__main__":
    my_dataset = MyDataset()
    print(my_dataset.train_dataset[0])