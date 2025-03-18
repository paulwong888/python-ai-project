import json
from a01_contant import *
from openai import OpenAI
from dotenv import load_dotenv
from datasets import load_dataset

"""
{
  "source": "synthetic_math",
  "problem": "Suppose that $g(x) = 5x - 3$. What is $g^{-1}(g^{-1}(14))$?",
  "solution": "First, we need to find the inverse function $g^{-1}(x)$. Given $g(x) = 5x - 3$, solve for $x$:\n\\[ y = 5x - 3 \\]\n\\[ y + 3 = 5x \\]\n\\[ x = \\frac{y + 3}{5} \\]\nThus, $g^{-1}(x) = \\frac{x + 3}{5}$.\n\nNow, apply $g^{-1}$ twice to the given value $14$:\n\\[ g^{-1}(14) = \\frac{14 + 3}{5} = \\frac{17}{5} \\]\n\\[ g^{-1}\\left(\\frac{17}{5}\\right) = \\frac{\\frac{17}{5} + 3}{5} = \\frac{\\frac{17}{5} + \\frac{15}{5}}{5} = \\frac{32}{5 \\times 5} = \\frac{32}{25} \\]\n\nThus, $g^{-1}(g^{-1}(14)) = \\boxed{\\frac{32}{25}}$.",
  "messages": [
    {
      "content": "Suppose that $g(x) = 5x - 3$. What is $g^{-1}(g^{-1}(14))$?",
      "role": "user"
    },
    {
      "content": "First, we need to find the inverse function $g^{-1}(x)$. Given $g(x) = 5x - 3$, solve for $x$:\n\\[ y = 5x - 3 \\]\n\\[ y + 3 = 5x \\]\n\\[ x = \\frac{y + 3}{5} \\]\nThus, $g^{-1}(x) = \\frac{x + 3}{5}$.\n\nNow, apply $g^{-1}$ twice to the given value $14$:\n\\[ g^{-1}(14) = \\frac{14 + 3}{5} = \\frac{17}{5} \\]\n\\[ g^{-1}\\left(\\frac{17}{5}\\right) = \\frac{\\frac{17}{5} + 3}{5} = \\frac{\\frac{17}{5} + \\frac{15}{5}}{5} = \\frac{32}{5 \\times 5} = \\frac{32}{25} \\]\n\nThus, $g^{-1}(g^{-1}(14)) = \\boxed{\\frac{32}{25}}$.",
      "role": "assistant"
    }
  ]
}
"""
class DistillData():
    def __init__(self):
        load_dotenv(dotenv_path)
        self.client = OpenAI()
        dataset = load_dataset(data_path)
        self.train_dataset = dataset["train"]
        self.test_dataset = dataset["test"]
        print(len(self.test_dataset))

    def load_data(self, data_size: None):
        index = 0
        item = {}
        data_file = distill_data_path + "/distill_data.csv"
        with open(data_file, "w", encoding="utf-8") as file:
            for data in self.train_dataset:
                if data_size and index >= data_size:
                    break
                problem = data["problem"]
                print(problem)
                response = self.get_response(problem)
                print(response)
                item["instruction"] = problem
                item["input"] = ""
                item["output"] = response

                json.dump(item, file, ensure_ascii=False)
                file.write("\n")
                file.flush()
                index += 1

    def get_response(self, message):
        response = self.client.chat.completions.create(
            model = "deepseek-reasoner",
            messages = [
                {"role": "system", "content": "你是一个智能助手"},
                {"role": "user", "content": message}
            ],
            stream = False,
        )
        return response.choices[0].message.content
    
def test_json():
    item = {}
    item["instruction"] = "problem"
    item["input"] = ""
    item["output"] = "你是一个智能助手"

    item_str = json.dumps(item, ensure_ascii=False)
    print(item_str)

if __name__ == "__main__":
    test_json()
    distill_data = DistillData()
    # print(distill_data.get_response("你好"))
    distill_data.load_data(5000)