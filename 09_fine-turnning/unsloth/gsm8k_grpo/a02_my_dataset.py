from a00_constant import *
from datasets import load_dataset
from transformers import AutoTokenizer

"""
{
  "question": [
    "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
    "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?"
  ],
  "answer": [
    "How many clips did Natalia sell in May? ** Natalia sold 48/2 = <<48/2=24>>24 clips in May.\nHow many clips did Natalia sell altogether in April and May? ** Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May.\n#### 72",
    "How much does Weng earn per minute? ** Weng earns 12/60 = $<<12/60=0.2>>0.2 per minute.\nHow much did Weng earn? ** Working 50 minutes, she earned 0.2 x 50 = $<<0.2*50=10>>10.\n#### 10"
  ]
}
format to:

{
  "answer": [
    "# 72",
    "# 10"
  ],
  "prompt": [
    [
      {
        "content": "\nRespond in the following format:\n<reasoning>\n...\n</reasoning>\n<answer>\n...\n</answer>\n",
        "role": "system"
      },
      {
        "content": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
        "role": "user"
      }
    ],
    [
      {
        "content": "\nRespond in the following format:\n<reasoning>\n...\n</reasoning>\n<answer>\n...\n</answer>\n",
        "role": "system"
      },
      {
        "content": "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?",
        "role": "user"
      }
    ]
  ]
}

"""

class MyDataset():
    def __init__(self):
        my_dataset = load_dataset(
            path=dataset_dir
        )
            # remove_columns = ["question", "answer"]
        self.my_dataset = my_dataset.map(
            lambda x: self.format_prompt(x), 
        )

    def extract_hash_message(self, text: str) -> str | None:
        if "####" not in text:
            return None
        else:
            return text.split("###")[1].strip()

    def format_prompt(self, samples):
        return {
            "prompt" : [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": samples["question"]},
            ],
            "answer": self.extract_hash_message(samples["answer"])
        }

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    my_dataset = MyDataset()
    print(my_dataset.my_dataset)
    # print(my_dataset.my_dataset["train"][0:2])
    data =  my_dataset.my_dataset["test"][0]
    print(type(data))
    print(data["prompt"])
    print(tokenizer.apply_chat_template([data["prompt"]], tokenize=False))
    # {'question': ["Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?", 'A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?'], 'answer': ['# 18', '# 3'], 'prompt': [[{'content': '\nRespond in the following format:\n<reasoning>\n...\n</reasoning>\n<answer>\n...\n</answer>\n', 'role': 'system'}, {'content': "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?", 'role': 'user'}], [{'content': '\nRespond in the following format:\n<reasoning>\n...\n</reasoning>\n<answer>\n...\n</answer>\n', 'role': 'system'}, {'content': 'A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?', 'role': 'user'}]]}