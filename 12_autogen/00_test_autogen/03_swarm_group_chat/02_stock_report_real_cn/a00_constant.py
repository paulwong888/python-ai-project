from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily

load_dotenv("/home/paul/config/.env")


model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
# model_client = OpenAIChatCompletionClient(
#     model="deepseek-chat",
#     model_capabilities = {
#         "vision": False,
#         "function_calling": True,
#         "json_output": False,
#         "family": ModelFamily.R1,
#     },
# )