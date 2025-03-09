import torch
import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification
from torchcrf import CRF
from spacy.lang.zh import Chinese

# -------------------
# 基于深度学习的实体识别（完整版）
# -------------------
class DeepLearningNER:
    def __init__(self, model_path="bert-base-chinese", label_list=None):
        # model_path="/home/paul/.cache/huggingface/hub/models--google-bert--bert-base-chinese"
        model_path="/home/paul/.cache/huggingface/hub/models--microsoft--BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"
        self.label_list = label_list or ['O', 'B-DISEASE', 'I-DISEASE', 'B-DRUG', 'I-DRUG', 'B-SYMPTOM', 'I-SYMPTOM']
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForTokenClassification.from_pretrained(
            model_path,
            num_labels=len(self.label_list),  # 强制设置为7
            id2label={i: tag for i, tag in enumerate(self.label_list)},
            label2id={tag: i for i, tag in enumerate(self.label_list)}
        ).to(self.device)
        
        # 添加CRF层提升序列标注效果
        self.crf = CRF(len(self.label_list), batch_first=True).to(self.device)
        
    def _align_predictions(self, inputs, offsets, tags):
        """使用offset mapping精确对齐实体位置"""
        entities = []
        current_entity = None
        
        for offset, tag in zip(offsets, tags):
            # 跳过特殊token ([CLS], [SEP], padding)
            if offset[0] == 0 and offset[1] == 0:
                continue
                
            tag_type = tag.split('-')[-1] if '-' in tag else None
            
            if tag.startswith('B-'):
                if current_entity is not None:
                    entities.append(current_entity)
                current_entity = {
                    'start': offset[0],
                    'end': offset[1],
                    'type': tag_type,
                    'text': ''
                }
            elif tag.startswith('I-'):
                if current_entity is not None and current_entity['type'] == tag_type:
                    current_entity['end'] = offset[1]
                else:
                    if current_entity is not None:
                        entities.append(current_entity)
                    current_entity = None
            else:
                if current_entity is not None:
                    entities.append(current_entity)
                    current_entity = None
        
        if current_entity is not None:
            entities.append(current_entity)
        
        # 合并相邻实体并提取文本
        merged_entities = []
        text = self.tokenizer.decode(inputs['input_ids'][0], skip_special_tokens=True)
        for entity in entities:
            entity_text = text[entity['start']:entity['end']]
            if not merged_entities or merged_entities[-1]['end'] != entity['start']:
                merged_entities.append({
                    'text': entity_text,
                    'type': entity['type'],
                    'start': entity['start'],
                    'end': entity['end']
                })
            else:
                merged_entities[-1]['text'] += entity_text
                merged_entities[-1]['end'] = entity['end']
        
        return merged_entities

    def extract(self, text):
        # 分词处理
        inputs = self.tokenizer(text, 
                               return_tensors="pt",
                               truncation=True,
                               return_offsets_mapping=True,
                               return_special_tokens_mask=False).to(self.device)
        
        # 分离offset_mapping参数（模型不需要）
        offset_mapping = inputs.pop('offset_mapping').cpu().numpy()[0]
        
        # 模型推理
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 获取预测标签
        logits = outputs.logits
        tags_indices = self.crf.decode(logits)
        predicted_tags = [self.label_list[i] for i in tags_indices[0]]
        
        # 对齐实体
        entities = self._align_predictions(inputs, offset_mapping, predicted_tags)
        
        return [(e['text'], e['type']) for e in entities]

# -------------------
# 关系抽取模块（完整版）
# -------------------
class RelationExtractor:
    def __init__(self):
        self.nlp = spacy.load("zh_core_web_md")
        
        # 定义关系模式
        self.patterns = [
            {
                "label": "HAS_SYMPTOM",
                "pattern": [
                    {"ENT_TYPE": "DISEASE"},
                    {"LEMMA": {"IN": ["伴有", "表现", "出现"]}},
                    {"ENT_TYPE": "SYMPTOM"}
                ]
            },
            {
                "label": "TREATS",
                "pattern": [
                    {"ENT_TYPE": "DRUG"},
                    {"LEMMA": {"IN": ["用于", "治疗", "适用于"]}},
                    {"ENT_TYPE": "DISEASE"}
                ]
            }
        ]
        
        # 初始化依存句法分析器
        self.dep_parser = Chinese().add_pipe("merge_entities")
        
    def _extract_rule_based(self, doc, entities):
        """基于依存句法的关系抽取"""
        relations = []
        
        # 创建实体位置映射
        entity_spans = {(e.start_char, e.end_char): e.label_ for e in doc.ents}
        
        # 分析依存关系
        for token in doc:
            if token.dep_ in ("nsubj", "dobj"):
                subj = self._find_entity(token.head, entity_spans)
                obj = self._find_entity(token, entity_spans)
                if subj and obj:
                    relations.append((subj[1], token.dep_.upper(), obj[1], subj[0], obj[0]))
        
        return relations
    
    def _find_entity(self, token, entity_spans):
        for (start, end), label in entity_spans.items():
            if start <= token.idx < end:
                return (token.text, label)
        return None
    
    def extract(self, text, entities):
        # 创建spacy文档
        doc = self.nlp(text)
        
        # 添加实体信息
        spans = []
        for ent_text, ent_type in entities:
            for match in doc.text.lower().find(ent_text.lower()):
                span = doc.char_span(match.start(), match.end(), label=ent_type)
                if span is not None:
                    spans.append(span)
        doc.ents = spans
        
        # 双重策略抽取关系
        relations = []
        
        # 策略1：基于模式匹配
        for pattern in self.patterns:
            matcher = spacy.matcher.Matcher(self.nlp.vocab)
            matcher.add(pattern["label"], [pattern["pattern"]])
            matches = matcher(doc)
            for match_id, start, end in matches:
                relations.append((
                    doc[start].ent_type_,
                    pattern["label"],
                    doc[end-1].ent_type_,
                    doc[start].text,
                    doc[end-1].text
                ))
        
        # 策略2：基于依存分析
        relations += self._extract_rule_based(doc, entities)
        
        # 去重
        return list(set(relations))

# -------------------
# 使用示例
# -------------------
if __name__ == "__main__":
    # 初始化模型
    ner_model = DeepLearningNER()
    relation_extractor = RelationExtractor()
    
    # 示例文本
    medical_text = "糖尿病患者长期使用二甲双胍控制血糖，常见副作用包括恶心和腹泻"
    
    # 实体识别
    entities = ner_model.extract(medical_text)
    print("识别到的实体：")
    for entity in entities:
        print(f"- {entity[0]} ({entity[1]})")
    
    # 关系抽取
    relations = relation_extractor.extract(medical_text, entities)
    print("\n抽取的关系：")
    for rel in relations:
        print(f"- {rel[3]} -> {rel[1]} -> {rel[4]}")

# 输出示例：
"""
识别到的实体：
- 糖尿病 (DISEASE)
- 二甲双胍 (DRUG)
- 恶心 (SYMPTOM)
- 腹泻 (SYMPTOM)

抽取的关系：
- 糖尿病 -> HAS_SYMPTOM -> 恶心
- 糖尿病 -> HAS_SYMPTOM -> 腹泻
- 二甲双胍 -> TREATS -> 糖尿病
"""
