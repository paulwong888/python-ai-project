from datasets import load_dataset, Dataset

class MyDataset():
    def __init__(self):
        data_set_path = "/home/paul/.cache/huggingface/hub/datasets--Kedreamix--psychology-10k-Deepseek-R1-zh"
        data_set = load_dataset(data_set_path, split="train")
        self.data_set: Dataset = self.pre_processing(data_set)#.select(range(5))
        self.save()

    def format_prompt(self, samples: Dataset):
        inputs = samples["input"]
        reasoning_contents = samples["reasoning_content"]
        contents = samples["content"]
        all_messages = []
        for input, reasoning_content, content in zip(inputs, reasoning_contents, contents):
            messages = []
            user_message = dict(role = "user",content = input)
            assiant_message = dict(role = "assistant", content = f"<think>{reasoning_content}</think>{content}")
            messages.append(user_message)
            messages.append(assiant_message)
            all_messages.append(messages)
        return dict(messages = all_messages)

    def pre_processing(self, data_set: Dataset) -> Dataset:
        return data_set.map(
            lambda x: self.format_prompt(x),
            batched = True,
            remove_columns = ["input", "reasoning_content", "content"]
        )
    
    def save(self):
        # with open(, "w", encoding="utf-8") as file:
        self.data_set.to_json(f"09_fine-turnning/axolotl/01_psychological-consultant/data/train.json", orient="records", lines=True, force_ascii=False)

if __name__ == "__main__":
    my_dataset = MyDataset()
    my_dataset