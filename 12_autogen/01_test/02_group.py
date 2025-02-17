from autogen import config_list_from_json, UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

llm_config = {"config_list": config_list_from_json("/home/paul/config/OAI_CONFIG_LIST")}

user_proxy = UserProxyAgent(
    "user_proxy",
    human_input_mode="ALWAYS",
    code_execution_config={"last_n_messages": 2, "work_dir": "12_autogen/01_test/sources/group_chat"},
    system_message="A human admin who will give the idea and run the code provided by coder"
)

coder = AssistantAgent(
    "coder",
    llm_config=llm_config   
)

pm = AssistantAgent(
    "product_manager",
    llm_config=llm_config,
    system_message="You will help break down initial idea into a well scoped \
        requirement for the coder. Do not involve in future conversation or error fixing"
)

group_chat = GroupChat(
    agents=[user_proxy, coder, pm], messages=[],
    max_round=15
)

manager = GroupChatManager(
    groupchat=group_chat, llm_config=llm_config
)

user_proxy.initiate_chat(
    recipient=manager,
    message="Build a classic and basic pong game with 2 players in python"
)
