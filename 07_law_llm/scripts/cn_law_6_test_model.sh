curl -X POST http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json; charset=utf-8" \
-d '{
    "model": "/home/paul/.cache/huggingface/models/models--unsloth--llama-3-8b-Instruct-lawdata",
    "messages": [{"role": "user", "content": "甲公司与乙公司签订了合同，其中包含件战条款，并选定了中国仲栽协会作为仲裁机构。当纠纷发生后，甲公司请求伸裁解决， 但乙公司却表示仲帮协议无效，认为纠纷超出了法律规定的仲裁范围。这种情况下，仲裁协议是否有效?"}]
}'