
docker compose exec axolotl \
    axolotl inference /app/configs/advance_train.yml \
        --lora-model-dir="/app/output/Llama3_Storyteller" \
        --gradio \
        --load-in-8bit true \
        --gradio-server-name 0.0.0.0