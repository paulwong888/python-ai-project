    # --quantization fp8
    # --cpu-offload-gb 10
# model：LLM模型路径。
# tensor_parallel_size：并行处理的大小。
# gpu_memory_utilization：默认为0.9， cpu_swap_space默认4个G。若gpu_memory_utilization参数过小(分配的内存大小低于模型使用内存)或者过大(接近1.0)时，代码会崩溃。
# request_rate：请求速率
# max_num_seqs：一次推理最多能处理的sequences数量，默认值是256。max_num_seqs越大，能处理的请求数量就会越大，但提升也会有上限，不一定是越大越好：
# 2卡时，max_num_seqs设置为1024，相较于256，速度提升19%。
# 4卡时，max_num_seqs设置为2048，相较于256，速度提升35%；max_num_seqs设置为4096，相较于256，速度提升33%。
# max_model_len：模型的最大生成长度，包含prompt长度和generated长度。这个值需要根据实际情况输入。
# max_num_batched_tokens：一次推理最多能处理的tokens数量，默认值是2048。max_num_batched_tokens越大，能处理的tokens数量也就越大，但vllm内部会根据max_model_len自动计算max_num_batched_tokens，所以可以不设置这个值。

# --quantization {aqlm,awq,deepspeedfp,tpu_int8,fp8,fbgemm_fp8,modelopt,
# marlin,gguf,gptq_marlin_24,gptq_marlin,awq_marlin,gptq,
# compressed-tensors,bitsandbytes,qqq,hqq,experts_int8,
# neuron_quant,ipex,None}, 


# Linux系统
# 使用lsof命令：输入命令lsof -i:8000，该命令会列出8000端口的占用情况，包括占用该端口的程序名称、PID等信息。
# 使用netstat命令：输入命令netstat -tunlp | grep 8000，该命令会显示8000端口的监听情况以及对应的进程信息。
    # --quantization gptq \
    # --dtype auto \
    # --cpu-offload-gb 5 \
    # --quantization bitsandbytes \


nohup \
# vllm serve /home/paul/.cache/huggingface/models/models--unsloth--llama-3-8b-Instruct-lawdata \
vllm serve /home/paul/.cache/huggingface/models/models--unsloth--llama-3-8b-Instruct-lawdata-awq_w_only \
    --port 8080 \
    --gpu-memory-utilization 0.7 \
    --served-model-name llama-3-8b-Instruct-lawdata \
    --max_model_len 1072 \
    --quantization bitsandbytes \
    --load_format bitsandbytes \
< /dev/null >> vllm-output.log 2>&1 &
tail -f vllm-output.log