import datetime
from openai import OpenAI
from a00_constant import LLAMA3_LAW_PATH

open_ai = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="123"
)

messages="""
甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
这种情况下，仲裁协议是否有效?
"""
print(datetime.datetime.now())
response = open_ai.chat.completions.create(
    model=LLAMA3_LAW_PATH,
    messages=[
        {"role": "user", "content": messages}
    ]
)
print(response.choices[0].message)
print(datetime.datetime.now())