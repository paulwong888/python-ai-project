import asyncio
from a00_constant import model_client
from a02_agents import *
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console

selector_prompt = """
Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from {participants} to perform the next task.
Make sure the planner agent has assigned tasks before other agents start working.
Only select one agent.
"""

async def main(task: str):
    text_mention_termination = TextMentionTermination("TERMINATE")
    max_messages_termination = MaxMessageTermination(max_messages=25)
    termination = text_mention_termination | max_messages_termination

    team = SelectorGroupChat(
        [planning_agent, websearch_agent, data_analyst_agent],
        model_client = model_client,
        selector_prompt = selector_prompt,
        termination_condition = termination,
        allow_repeated_speaker = True
    )

    await Console(team.run_stream(task=task))

if __name__ == "__main__":
    # task = "Who was the Miami Heat player with the highest points in the 2006-2007 season, and what was the percentage change in his total rebounds between the 2007-2008 and 2008-2009 seasons?"
    task = "迈阿密热火队在2006-2007赛季得分最高的球员是谁，以及他在2007-2008赛季和2008-2009赛季之间的总篮板数的百分比变化是多少"
    asyncio.run(main(task))