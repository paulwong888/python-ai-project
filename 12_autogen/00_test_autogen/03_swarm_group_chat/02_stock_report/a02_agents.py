from a00_constant import model_client
from a01_tools import *
from autogen_agentchat.agents import AssistantAgent

planer_agent = AssistantAgent(
    "planer_agent",
    handoffs = ["financial_analyst_agent", "news_analyst_agent", "writer_agent"],
    model_client = model_client,
    system_message = """You are a research planning coordinator.
    Coordinate market research by delegating to specialized agents:
    - Financial Analyst: For stock data analysis
    - News Analyst: For news gathering and analysis
    - Writer: For compiling final report
    Always send your plan first, then handoff to appropriate agent.
    Always handoff to a single agent at a time.
    Use TERMINATE when research is complete.""",
)

financial_analyst_agent = AssistantAgent(
    "financial_analyst_agent",
    tools = [get_stock_data],
    handoffs = ["planer_agent"],
    model_client = model_client,
    system_message = """You are a financial analyst.
    Analyze stock market data using the get_stock_data tool.
    Provide insights on financial metrics.
    Always handoff back to planner when analysis is complete.""",
)

news_analyst_agent = AssistantAgent(
    "news_analyst_agent",
    tools = [get_news],
    handoffs = ["planer_agent"],
    model_client = model_client,
    system_message = """You are a news analyst.
    Gather and analyze relevant news using the get_news tool.
    Summarize key market insights from news.
    Always handoff back to planner when analysis is complete.""",
)

writer_agent = AssistantAgent(
    "writer_agent",
    handoffs = ["planer_agent"],
    model_client = model_client,
    system_message = """You are a financial report writer.
    Compile research findings into clear, concise reports.
    Always handoff back to planner when writing is complete.""",
)