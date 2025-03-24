import torch
from transformers import BitsAndBytesConfig, AutoProcessor, AutoModelForImageTextToText
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

def main():
    model_id = "./gemma3-4B"   # or gemma-3-4b-it
    device_cap = torch.cuda.get_device_capability()[0]
    if device_cap < 8:
        raise ValueError("Need GPU with bfloat16 support (e.g. A100).")

    model_kwargs = dict(
        attn_implementation="eager",  # 官方示例
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    # BitsAndBytesConfig int-4
    model_kwargs["quantization_config"] = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=model_kwargs["torch_dtype"],
        bnb_4bit_quant_storage=model_kwargs["torch_dtype"]
    )

    # 2) Processor
    print("Loading model ...")
    model = AutoModelForImageTextToText.from_pretrained(
        model_id,
        **model_kwargs
    )
    processor = AutoProcessor.from_pretrained("./gemma3-4B")
    # 
    # 3)(QLoRA)
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.05,
        r=16,
        bias="none",
        target_modules="all-linear",  # QLoRA: all
        task_type="CAUSAL_LM",
        modules_to_save=["lm_head","embed_tokens"],  
    )

    # 4) SFTConfig
    sft_args = SFTConfig(
        output_dir="gemma-output-flickr30k_10k",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        gradient_checkpointing=True,
        optim="adamw_torch_fused",
        logging_steps=5,
        save_strategy="epoch",
        learning_rate=2e-4,
        bf16=True,
        max_grad_norm=0.3,
        warmup_ratio=0.03,
        lr_scheduler_type="constant",
        push_to_hub=False,    
        report_to="tensorboard",
        gradient_checkpointing_kwargs={
            "use_reentrant": False
        },
        dataset_text_field="",  # dummy
        dataset_kwargs={"skip_prepare_dataset": True},
        # deepspeed="ds_zero2_no_offload.json"
    )
    sft_args.remove_unused_columns = False
    # 5) 
    data_path = "my_flickr_full_chat.json"  
    train_dataset = load_my_flickr_dataset(data_path, split="train")
    # 
    # val_dataset = load_my_flickr_dataset(data_path, split="val")
    # 6) SFTTrainer
    trainer = SFTTrainer(
        model=model,
        args=sft_args,
        train_dataset=train_dataset,
        peft_config=peft_config,
        processing_class=processor,    
        data_collator=lambda batch: collate_fn(batch, processor, image_root="/data/rzr/flickr30k/flickr30k-images") 
    )
    trainer.train()

    trainer.save_model()

    from peft import PeftModel
    merged_model = PeftModel.from_pretrained(model, sft_args.output_dir).merge_and_unload()
    merged_model.save_pretrained("my_merged_model_10k")