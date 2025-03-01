from a00_constant import model_client
from a01_tools import *
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent

planning_agent = AssistantAgent(
    "PlanningAgent",
    description = "An agent for planning tasks, this agent should be the first to engage when given a new task.",
    model_client = model_client,
    system_message="""
    You are a planning agent.
    Your job is to break down complex tasks into smaller, manageable subtasks.
    Your team members are:
        WebSearchAgent: Searches for information
        DataAnalystAgent: Performs calculations

    You only plan and delegate tasks - you do not execute them yourself.

    When assigning tasks, use this format:
    1. <agent> : <task>

    After all tasks are complete, summarize the findings and end with "TERMINATE".
    """
)

websearch_agent = AssistantAgent(
    "WebSearchAgent",
    description = "An agent for searching information on the web.",
    tools = [search_web_tool],
    model_client = model_client,
    system_message = """
    You are a web search agent.
    Your only tool is search_tool - use it to find information.
    You make only one search call at a time.
    Once you have the results, you never do calculations based on them.
    """
)

data_analyst_agent = AssistantAgent(
    "DataAnalystAgent",
    description = "An agent for performing calculations.",
    tools = [percentage_change_tool],
    model_client = model_client,
    system_message="""
    You are a data analyst.
    Given the tasks you have been assigned, you should analyze the data and provide results using the tools provided.
    If you have not seen the data, ask for it.
    """
)