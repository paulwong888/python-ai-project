import re, wandb
from a00_constant import *
from a02_my_dataset import MyDataset
from a01_my_model import MyModel
from trl import GRPOConfig, GRPOTrainer
from unsloth import FastLanguageModel, PatchFastRL
PatchFastRL("GRPO", FastLanguageModel)

class MyTrainer():

    def __init__(self):
        wandb.login(key=wandb_key)
        run = wandb.init(
            project='grpo-train-Qwen2.5-7B-Instruct on gsmk8 Dataset', 
            job_type="training", 
            anonymous="allow"
        )
        my_peft_model = MyModel().peft_my_model
        my_dataset = MyDataset().my_dataset["train"]
        grpo_config = GRPOConfig(
            use_vllm = True, # use vLLM for fast inference!
            learning_rate = 5e-6,
            # adam_beta1 = 0.9,
            # adam_beta2 = 0.99,
            weight_decay = 0.1,
            warmup_ratio = 0.1,
            lr_scheduler_type = "cosine",
            optim = "paged_adamw_8bit",
            logging_steps = 1,
            bf16 = is_bfloat16_supported(),
            fp16 = not is_bfloat16_supported(),
            per_device_train_batch_size = 1,
            gradient_accumulation_steps = 1, # Increase to 4 for smoother training
            num_generations = 6, # Decrease if out of memory
            max_prompt_length = 256,
            max_completion_length = 200,
            # num_train_epochs = 1, # Set to 1 for a full training run
            max_steps = 250,
            save_steps = 250,
            max_grad_norm = 0.1,
            report_to = report_to, # Can use Weights & Biases
            output_dir = output_dir,
        )
        self.grpo_trainer = GRPOTrainer(
            model = my_peft_model,
            args = grpo_config,
            train_dataset = my_dataset,
            reward_funcs = [
                self.xmlcount_reward_func,
                self.soft_format_reward_func,
                self.strict_format_reward_func,
                self.int_reward_func,
                self.correctness_reward_func
            ]
        )

    def train(self):
        self.grpo_trainer.train()

    def extract_xml_answer(self, text: str) -> str:
        answer = text.split("<answer>")[-1]
        answer = answer.split("</answer>")[0]
        return answer.strip()
    
    # Reward functions
    def correctness_reward_func(self, prompts, completions, answer, **kwargs) -> list[float]:
        responses = [completion[0]['content'] for completion in completions]
        q = prompts[0][-1]['content']
        extracted_responses = [self.extract_xml_answer(r) for r in responses]
        print('-'*20, f"Question:\n{q}", f"\nAnswer:\n{answer[0]}", f"\nResponse:\n{responses[0]}", f"\nExtracted:\n{extracted_responses[0]}")
        return [2.0 if r == a else 0.0 for r, a in zip(extracted_responses, answer)]

    def int_reward_func(self, completions, **kwargs) -> list[float]:
        responses = [completion[0]['content'] for completion in completions]
        extracted_responses = [self.extract_xml_answer(r) for r in responses]
        return [0.5 if r.isdigit() else 0.0 for r in extracted_responses]

    def strict_format_reward_func(self, completions, **kwargs) -> list[float]:
        """Reward function that checks if the completion has a specific format."""
        pattern = r"^<reasoning>\n.*?\n</reasoning>\n<answer>\n.*?\n</answer>\n$"
        responses = [completion[0]["content"] for completion in completions]
        matches = [re.match(pattern, r) for r in responses]
        return [0.5 if match else 0.0 for match in matches]

    def soft_format_reward_func(self, completions, **kwargs) -> list[float]:
        """Reward function that checks if the completion has a specific format."""
        pattern = r"<reasoning>.*?</reasoning>\s*<answer>.*?</answer>"
        responses = [completion[0]["content"] for completion in completions]
        matches = [re.match(pattern, r) for r in responses]
        return [0.5 if match else 0.0 for match in matches]

    def count_xml(self, text) -> float:
        count = 0.0
        if text.count("<reasoning>\n") == 1:
            count += 0.125
        if text.count("\n</reasoning>\n") == 1:
            count += 0.125
        if text.count("\n<answer>\n") == 1:
            count += 0.125
            count -= len(text.split("\n</answer>\n")[-1])*0.001
        if text.count("\n</answer>") == 1:
            count += 0.125
            count -= (len(text.split("\n</answer>")[-1]) - 1)*0.001
        return count

    def xmlcount_reward_func(self, completions, **kwargs) -> list[float]:
        contents = [completion[0]["content"] for completion in completions]
        return [self.count_xml(c) for c in contents]
    
if __name__ == "__main__":
    MyTrainer().train()