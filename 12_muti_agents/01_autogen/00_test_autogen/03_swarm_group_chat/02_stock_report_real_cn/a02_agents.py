from a00_constant import model_client
# from a01_tools_2 import *
from a01_tools import *
from autogen_agentchat.agents import AssistantAgent

planer_agent = AssistantAgent(
    "planer_agent",
    handoffs = ["financial_analyst_agent", "news_analyst_agent", "writer_agent"],
    model_client = model_client,
    system_message = """你是一名研究规划协调员。
    通过委派给专业智能体来协调市场研究：
    - 金融分析师：负责股票数据分析
    - 新闻分析师：负责新闻收集和分析
    - 撰写员：负责编写最终报告
    始终先发送你的计划，然后再移交给适当的智能体。
    每次只能移交给一个智能体。
    当研究完成时输出 TERMINATE。""",
)

financial_analyst_agent = AssistantAgent(
    "financial_analyst_agent",
    tools = [get_stock_data],
    handoffs = ["planer_agent"],
    model_client = model_client,
    system_message = """你是一名金融分析师。
    使用 get_stock_data 工具分析股市数据。
    提供金融指标的深入见解。
    分析完成后务必移交回规划协调员。""",
)

news_analyst_agent = AssistantAgent(
    "news_analyst_agent",
    tools = [get_news],
    handoffs = ["planer_agent"],
    model_client = model_client,
    system_message = """你是一名新闻分析师。
    使用 get_news 工具收集和分析相关新闻。
    总结新闻中的关键市场见解。
    分析完成后务必移交回规划协调员。""",
)

writer_agent = AssistantAgent(
    "writer_agent",
    handoffs = ["planer_agent"],
    model_client = model_client,
    system_message = """你是一名财经报告撰写员。
    将研究发现编译成清晰简洁的报告。
    撰写完成后务必移交回规划协调员。""",
)