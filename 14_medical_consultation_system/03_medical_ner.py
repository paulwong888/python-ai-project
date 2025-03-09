from transformers import pipeline

model_path = "/home/paul/.cache/huggingface/hub/models--medicalai--ClinicalBERT"
model_path = "/home/paul/.cache/huggingface/hub/models--blaze999--Medical-NER"
model_path = "/home/paul/.cache/huggingface/hub/models--iioSnail--bert-base-chinese-medical-ner"

text = "45 year old woman diagnosed with CAD"
text = "患者有高血压和糖尿病，建议使用洛卡特普和二甲双胍。"
# text = "糖尿病常用药物包括二甲双胍和胰岛素，症状有多饮、多尿。建议就诊内分泌科。"
# pipe = pipeline("token-classification", model=model_path, aggregation_strategy='simple')
# result = pipe(text)
# print(result)


def format_outputs(sentences, outputs):
        preds = []
        for i, pred_indices in enumerate(outputs):
            words = []
            start_idx = -1
            end_idx = -1
            flag = False
            for idx, pred_idx in enumerate(pred_indices):
                if pred_idx == 1:
                    start_idx = idx
                    flag = True
                    continue

                if flag and pred_idx != 2 and pred_idx != 3:
                    # 出现了不应该出现的index
                    print("Abnormal prediction results for sentence", sentences[i])
                    start_idx = -1
                    end_idx = -1
                    continue

                if pred_idx == 3:
                    end_idx = idx

                    words.append({
                        "start": start_idx,
                        "end": end_idx + 1,
                        "word": sentences[i][start_idx:end_idx+1]
                    })
                    start_idx = -1
                    end_idx = -1
                    flag = False
                    continue

            preds.append(words)

        return preds

from transformers import AutoModelForTokenClassification, BertTokenizerFast

tokenizer = BertTokenizerFast.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

# sentences = ["瘦脸针、水光针和玻尿酸详解！", "半月板钙化的病因有哪些？"]
sentences = [text]
inputs = tokenizer(sentences, return_tensors="pt", padding=True, add_special_tokens=False)
outputs = model(**inputs)
outputs = outputs.logits.argmax(-1) * inputs['attention_mask']

print(outputs)

print(format_outputs(sentences, outputs))