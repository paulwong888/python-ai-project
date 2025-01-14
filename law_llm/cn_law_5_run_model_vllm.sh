    # --dtype float16 \
    # --quantization fp8
# model：LLM模型路径。
# tensor_parallel_size：并行处理的大小。
# gpu_memory_utilization：默认为0.9， cpu_swap_space默认4个G。若gpu_memory_utilization参数过小(分配的内存大小低于模型使用内存)或者过大(接近1.0)时，代码会崩溃。
# request_rate：请求速率
# max_num_seqs：一次推理最多能处理的sequences数量，默认值是256。max_num_seqs越大，能处理的请求数量就会越大，但提升也会有上限，不一定是越大越好：
# 2卡时，max_num_seqs设置为1024，相较于256，速度提升19%。
# 4卡时，max_num_seqs设置为2048，相较于256，速度提升35%；max_num_seqs设置为4096，相较于256，速度提升33%。
# max_model_len：模型的最大生成长度，包含prompt长度和generated长度。这个值需要根据实际情况输入。
# max_num_batched_tokens：一次推理最多能处理的tokens数量，默认值是2048。max_num_batched_tokens越大，能处理的tokens数量也就越大，但vllm内部会根据max_model_len自动计算max_num_batched_tokens，所以可以不设置这个值。
vllm serve /home/paul/.cache/huggingface/models/models--unsloth--llama-3-8b-Instruct-lawdata \
    --gpu-memory-utilization 0.7 \
    --max_model_len 40960 \
    --cpu-offload-gb 10