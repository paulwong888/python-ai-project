from a01_contant import *
from datasets import load_dataset

class MyDataset():
    def __init__(self):
        self.dataset = load_dataset(distill_data_path, split="train")
        self.dataset = self.dataset.rename_column("instruction", "prompt") \
                                   .rename_column("output", "completion") \
                                   .remove_columns("input")

if __name__ == "__main__":
    my_dataset = MyDataset()
    dataset = my_dataset.dataset
    print(dataset)