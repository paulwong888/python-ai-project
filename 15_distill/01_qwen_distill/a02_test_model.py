from a01_contant import *
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen2ForCausalLM, Qwen2Tokenizer

class MyModel():
    def __init__(self):
        self.tokenizer: Qwen2Tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model: Qwen2ForCausalLM = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="auto",
        )

    def generate(self, message):
        prompt = [
            {"role": "system", "content": "you are a helpfull assisitant."},
            {"role": "user", "content": message}
        ]
        text = self.tokenizer.apply_chat_template(
            prompt,
            tokenize=False,
            add_generation_prompt=True
        )
        model_input = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_input,
            max_new_tokens = 512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_input, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response
    
if __name__ == "__main__":
    my_model = MyModel()
    print(my_model.generate("请证明根号2是无理数"))

    """
    user
    请证明根号2是无理数
    assistant
    要证明根号2是一个无理数，我们可以使用反证法。假设根号2是有理数，那么它可以表示为两个整数a和b的比值，即：

    √2 = a/b

    其中a和b都是整数，并且b不等于0。

    接下来我们对这个等式两边进行平方：

    (√2)^2 = (a/b)^2

    这简化为：

    2 = a^2 / b^2

    现在我们将等式乘以b^2：

    2 * b^2 = a^2

    从这里可以看出，a^2是一个偶数（因为2是一个偶数）。由于偶数的平方也一定是偶数，所以a也是一个偶数。设a=2k，其中k也是整数。

    将a=2k代入原方程中得到：

    2 = (2k)^2 / b^2

    化简得：

    2 = 4k^2 / b^2

    从而：

    b^2 = 2k^2

    同样地，b也是一个偶数（因为2k^2是一个偶数）。但是，这与我们的假设矛盾了，因为我们假设a和b都是奇数或至少一个为奇数。

    因此，根据反证法，我们得出结论：根号2不能被表示为两个整数之比，也就是说根号2不是一个有理数，而是无理数。
    """
