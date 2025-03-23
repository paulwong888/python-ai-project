import datasets
from a00_constant import dataset_name, model_name, train_prompt_style
from datasets import load_dataset, Dataset
from transformers import LlamaTokenizerFast

class MyDataset():
    def __init__(self):
        super(MyDataset, self).__init__()
        tokenizer = LlamaTokenizerFast.from_pretrained(model_name)
        self.EOS_TOKEN = tokenizer.eos_token  # Must add EOS_TOKEN
        self.dataset = load_dataset("json", "en", data_dir=dataset_name, split="train[0:500]")
        self.dataset = self.pre_process_data(self.dataset)
        print(type(self.dataset))

    def pre_process_data(self, dataset):
        return dataset.map(
            lambda x: self.format_prompt(x),
            batched = True,
            # remove_columns = ["instruction", "input", "output"]
            remove_columns = ["Question", "Complex_CoT", "Response"]
        )

    def format_prompt(self, samples):
        inputs = samples["Question"]
        cots = samples["Complex_CoT"]
        outputs = samples["Response"]
        texts = []
        for input, cot, output in zip(inputs, cots, outputs):
            text = train_prompt_style.format(input, cot, output) + self.EOS_TOKEN
            texts.append(text)
        return {"text": texts}
    
    def get_dataset(self):
        return self.dataset
    
if __name__ == "__main__":
    my_dataset = MyDataset()
    print(my_dataset.get_dataset()[0])