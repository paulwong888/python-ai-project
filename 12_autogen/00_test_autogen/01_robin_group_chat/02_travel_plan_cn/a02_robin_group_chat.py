import asyncio
from a01_agents import *
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

async def robin_group_chat_main(task: str):
    termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat(
        [planner_agent, local_agent, language_agent, travel_summary_agent],
        termination_condition = termination
    )

    await Console(team.run_stream(task=task))

if __name__ == "__main__":
    task = "制定一个日本5日游计划."
    asyncio.run(robin_group_chat_main(task))