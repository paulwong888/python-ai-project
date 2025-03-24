import torch, os
import torch.distributed as dist

def main():
    dist.init_process_group(backend="nccl", init_method="env://")
    local_rank = os.getenv("LOCAL_RANK")
    torch.cuda.set_device(local_rank)

if __name__ == "__main__":
    main()