import datetime
from openai import OpenAI
from a00_constant import LLAMA3_LAW_VLLM_ID, VLLM_COMPLETIONS_URL

class VllmClient():
    def __init__(self):
        # self.model_name = LLAMA3_LAW_VLLM_ID
        self.open_ai = OpenAI(
            base_url=VLLM_COMPLETIONS_URL,
            api_key="sk-fastgpt"
        )
        self.model_name = models = self.open_ai.models.list().data[0].id

    def completions(self, message, for_web=True):
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
                if for_web:
                    chunk_message += chunk.choices[0].delta.content
                else:
                    chunk_message = chunk.choices[0].delta.content
                yield chunk_message
        else:
            return response

if __name__ == "__main__":
    import asyncio
    vllm_client = VllmClient()

    messages="""甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
        当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
        这种情况下，仲裁协议是否有效?"""
    response = vllm_client.completions(messages, False)
    result = []
    for chunk in response:
        result.append(chunk)
        print(chunk, end="", flush=True)
        # if chunk:
        # else:
        #     print(result[:-1])
        #     break
