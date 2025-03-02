from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv("/home/paul/config/.env")


model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")