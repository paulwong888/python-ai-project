LLAMA3_LAW_PATH = "/home/paul/.cache/huggingface/models/models--unsloth--llama-3-8b-Instruct-lawdata"
LLAMA3_LAW_AWQ_PATH = "/home/paul/.cache/huggingface/models/Llama3_CN_Law_Merged_awq"
DEEPSEEK_32B_PATH = "/home/paul/.cache/huggingface/models/DeepSeek-R1-Distill-Qwen-32B"
GEMMA_3_12B_IT_PATH = "/home/paul/.cache/huggingface/models/models--google--gemma-3-12b-it"
GEMMA_3_27B_IT_PATH = "/home/paul/.cache/huggingface/models/models--google--gemma-3-27b-it"
GEMMA_3_12B_IT_4BIT_PATH = "/home/paul/.cache/huggingface/models/models--unsloth--gemma-3-12b-it-bnb-4bit"


LLAMA3_LAW_VLLM_ID = "llama-3-8b-Instruct-lawdata"
LLAMA3_LAW_VLLM_ID = "llama-3-8b-Instruct-lawdata"
QWEN_REPO_ID = "Qwen/Qwen2.5-7B-Instruct"
# VLLM_COMPLETIONS_URL = "http://192.168.0.106:8000/v1" #pure vllm
# VLLM_COMPLETIONS_URL = "http://192.168.0.106:82/v1" #one-api nginx
VLLM_COMPLETIONS_URL = "http://192.168.0.101:85/v1" #one-api nginx


LAW_MESSAGE = """
甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。
当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。
这种情况下，仲裁协议是否有效?
"""