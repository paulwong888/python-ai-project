from a00_constant import *
from a01_my_dataset import MyDataset
from a02_my_model import MyModel
from trl import SFTConfig, SFTTrainer
from transformers import EarlyStoppingCallback, TrainerCallback

class MyTrainer():
    def __init__(self):
        self.init_torch_mesh()
        my_dataset = MyDataset()
        my_model = MyModel()
        sft_config =SFTConfig(
            output_dir, True,
            per_device_train_batch_size = 2,
            per_device_eval_batch_size = 2,
            gradient_accumulation_steps = 4,
            gradient_checkpointing = True,
            # num_train_epochs = 5,
            # eval setting
            eval_strategy = "steps", # 每个 epoch 结束后进行评估
            eval_steps = 1,
            save_strategy = "steps",
            save_steps = 1,
            metric_for_best_model = "eval_loss", # 监控验证集上的损失
            load_best_model_at_end = True, # 训练结束后加载最佳模型
            greater_is_better = False, # 如果监控的是损失，设置为 False

            # warmup_ratio=0.03,                  # 学习率预热比例
            # lr_scheduler_type="cosine",         # 余弦学习率调度
            # weight_decay=0.01,                  # 权重衰减防过拟合
            # max_grad_norm=0.3,                  # 梯度裁剪阈值
            
            # greater_is_better = False, # 如果监控的是损失，设置为 False
            # lr_scheduler_type=a,
            # fp16 = True,
            # data_seed = zero3_path,
            logging_steps = 1,
            logging_strategy="steps",  # 按步骤输出日志
            report_to="all",  # 将日志输出到 TensorBoard
            # log_level="info",  # 设置日志级别为 INFO
            logging_dir="./logs",

            # 限制步数快速验证流程
            max_steps = 1,

            # 分布式训练配置
            dataloader_num_workers = 4,
            ddp_find_unused_parameters = False,
        )
        # self.model = my_model.get_my_peft_model(),
        self.sft_trainer = SFTTrainer(
            # model = self.model,
            # processing_class = my_model.tokenizer,
            model =  my_model.get_my_peft_model(),
            train_dataset = my_dataset.train_dataset,
            eval_dataset = my_dataset.val_dataset,
            args = sft_config,
            # peft_config = peft_config,
            callbacks=[
                EarlyStoppingCallback(early_stopping_patience = 5),
                # LossLoggingCallback(),    
            ],
        )

    def train(self):
        print("Starting training...")
        # for name, param in self.model.named_parameters():
        #     if not param.requires_grad:
        #         print(f"Parameter {name} is frozen and will not be updated.")
        # eval_results = self.sft_trainer.evaluate()
        # print("=====>" + eval_results)  # 检查输出是否包含 metric_for_best_model 的键
        # self.sft_trainer.deepspeed = None
        self.sft_trainer.train()
        self.sft_trainer.save_model(adapter_dir)

    def init_torch_mesh(self):
        import torch, os
        import torch.distributed as dist
        from torch.distributed._tensor import DeviceMesh

        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"  # 减少碎片化
        print("初始化分布式环境 ------>")
        # 初始化分布式环境
        dist.init_process_group(backend="nccl", init_method="env://")
        local_rank = int(os.environ['LOCAL_RANK'])
        torch.cuda.set_device(local_rank)

        # 创建全局设备网格 (假设使用4卡)
        # device_mesh = DeviceMesh("cuda", torch.arange(2))

class LossLoggingCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs and "loss" in logs:
            print(f"Step {state.global_step}: Loss = {logs['loss']}")

if __name__ == "__main__":
    my_trainer = MyTrainer()
    my_trainer.train()
