import asyncio
from a02_agents import *
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.ui import Console

async def swarm_group_chat_main(task: str):

    termination = TextMentionTermination("TERMINATE")

    team = Swarm(
        [planer_agent, financial_analyst_agent, news_analyst_agent, writer_agent],
        termination_condition = termination,
    )

    await Console(team.run_stream(task=task))

if __name__ == "__main__":
    # task = "Conduct market research for TSLA stock"
    task = "对特斯拉(TSLA)股票进行市场调查, 用中文回答"
    asyncio.run(swarm_group_chat_main(task))