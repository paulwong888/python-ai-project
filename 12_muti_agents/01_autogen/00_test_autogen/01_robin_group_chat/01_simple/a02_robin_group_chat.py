import asyncio
from a01_agents import *
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

async def round_robing_group_chat_main(task: str):

    text_mention_termination = TextMentionTermination("APPROVE")

    team = RoundRobinGroupChat(
        [primary_agent, critic_agent],
        termination_condition = text_mention_termination
    )
    # await Console(team.run_stream(task=task))
    stream = team.run_stream(task=task)
    async for message in stream:
        print(message.content, end="")

if __name__ == "__main__":
    # task = "Write a short poem about the fall season."
    task = "写一首关于秋天的短诗"
    asyncio.run(round_robing_group_chat_main(task))