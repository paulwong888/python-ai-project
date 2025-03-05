from a00_constant import model_client
from a01_tools import refund_flight
from autogen_agentchat.agents import AssistantAgent

travel_agent = AssistantAgent(
    "travel_agent",
    handoffs = ["flights_refunder_agent", "user"],
    model_client = model_client,
    system_message = """
    You are a travel agent.
    The flights_refunder is in charge of refunding flights.
    If you need information from the user, you must first send your message, then you can handoff to the user.
    Use TERMINATE when the travel planning is complete.
    """
)

flights_refunder_agent = AssistantAgent(
    "flights_refunder_agent",
    handoffs = ["travel_agent", "user"],
    tools = [refund_flight],
    model_client = model_client,
    system_message = """
    You are an agent specialized in refunding flights.
    You only need flight reference numbers to refund a flight.
    You have the ability to refund a flight using the refund_flight tool.
    If you need information from the user, you must first send your message, then you can handoff to the user.
    When the transaction is complete, handoff to the travel agent to finalize.
    """,
)