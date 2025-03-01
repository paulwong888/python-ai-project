from a00_constant import *
from autogen_agentchat.agents import AssistantAgent

primary_agent = AssistantAgent(
    "PrimaryAgent",
    model_client = model_client,
    system_message = "You are a helpful AI assistant."
)

critic_agent = AssistantAgent(
    "critic_agent",
    model_client = model_client,
    system_message = "Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed."
)