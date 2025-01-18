AWQ_HOME=/home/paul/paulwong/work/workspaces/llm-awq
python -m $AWQ_HOME/awq/entry \
    --model_path /home/paul/paulwong/work/workspaces/python-ai-project/law_llm/models/models--unsloth--llama-3-8b-Instruct-lawdata \
    --w_bit 4 --q_group_size 128 \
    --run_awq --dump_awq awq_cache/llama3-8b-w4-g128.pt