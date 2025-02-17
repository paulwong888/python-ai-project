from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

llm_config = {"config_list": config_list_from_json("/home/paul/config/OAI_CONFIG_LIST")}

assiant_agent = AssistantAgent("assiant_agent", llm_config=llm_config)

user_agent = UserProxyAgent("user_agent", code_execution_config={"work_dir": "12_autogen/01_test/sources"})

user_agent.initiate_chat(
    assiant_agent,
    message="Plot a chart of NVDA and TESLA stock price change YTD."
)
