import asyncio
from a02_agents import *
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.ui import Console

async def swarm_group_chat_main(task: str) -> str:
    
    termination = HandoffTermination(target="user") | TextMentionTermination("TERMINATE")

    team = Swarm(
        [travel_agent, flights_refunder_agent],
        termination_condition = termination
    )

    task_result = await Console(team.run_stream(task=task))
    last_message = task_result.messages[-1]

    print(f"----> {last_message}")

    while isinstance(last_message, HandoffMessage) and last_message.target == "user":
        user_message = input("User: ")

        task_result = await Console(
            team.run_stream(task=HandoffMessage(source="user", target=last_message.source, content=user_message))
        )
        last_message = task_result.messages[-1]

if __name__ == "__main__":
    task = "I need to refund my flight."
    asyncio.run(swarm_group_chat_main(task))