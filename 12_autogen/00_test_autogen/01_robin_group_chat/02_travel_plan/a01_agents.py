from a00_constant import model_client
from autogen_agentchat.agents import AssistantAgent

planner_agent = AssistantAgent(
    "planner_agent",
    model_client = model_client,
    description = "一个能够帮助规划行程的智能助手",
    system_message = "你是一个能够根据用户需求提供旅行规划建议的智能助手。"
)

local_agent = AssistantAgent(
    "local_agent",
    description = "一个能够推荐当地活动和景点的在地助手",
    model_client = model_client,
    system_message = "你是一个能够为用户推荐地道有趣的当地活动和景点的智能助手，可以充分利用所提供的任何背景信息。"
)

language_agent = AssistantAgent(
    "language_agent",
    description = "一个能够提供目的地语言建议的智能助手",
    model_client = model_client,
    system_message = "你是一个能够审查旅行计划的智能助手，负责就如何最好地应对目的地的语言或沟通挑战提供重要/关键提示。如果计划中已经包含了语言提示，你可以说明计划是令人满意的，并解释原因。"
)

travel_summary_agent = AssistantAgent(
    "travel_summary_agent",
    description = "一个能够总结旅行计划的智能助手",
    model_client = model_client,
    system_message = "你是一个能够整合其他助手的所有建议和意见并提供详细最终旅行计划的智能助手。你必须确保最终计划是完整且连贯的。你的最终回复必须是完整的计划。当计划完整且所有观点都已整合后，你可以回复'TERMINATE'。"
)