import datetime
from openai import OpenAI
from a00_constant import LLAMA3_LAW_VLLM_ID, VLLM_COMPLETIONS_URL

class VllmClient():
    def __init__(self):
        self.model_name = LLAMA3_LAW_VLLM_ID
        self.open_ai = OpenAI(
            base_url=VLLM_COMPLETIONS_URL,
            api_key="123"
        )

    def completions(self, message):
        stream = True
        response = self.open_ai.chat.completions.create(
            model = self.model_name,
            messages=[
                {"role": "system", "content": "You are an assistant who provides precise and direct answers in Chinese "},
                {"role": "user", "content": message}
            ],
            stream = True
        )
        if stream:
            chunk_message = ""
            for chunk in response:
                chunk_message += chunk.choices[0].delta.content
                yield chunk_message
        else:
            return response

if __name__ == "__main__":
    import asyncio
    vllm_client = VllmClient()

    messages="""甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
        当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
        这种情况下，仲裁协议是否有效?"""
    response = vllm_client.completions(messages)
    result = []
    for chunk in response:
        if chunk:
            result.append(chunk)
        else:
            print(result[:-1])
            break
