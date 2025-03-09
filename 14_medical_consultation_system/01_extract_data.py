import pandas as pd
import re, spacy, json
from py2neo import Graph, Node, Relationship
import spacy.displacy

"""
  {
    "entities": [
      [
        "drug",
        "示例降糖片"
      ],
      [
        "chemical",
        "盐酸二甲双胍"
      ],
      [
        "company",
        "示例制药有限公司"
      ]
    ],
    "relations": [
      [
        "drug",
        "contains_chemical",
        "chemical",
        "示例降糖片",
        "盐酸二甲双胍"
      ],
      [
        "drug",
        "produced_by",
        "company",
        "示例降糖片",
        "示例制药有限公司"
      ],
      [
        "drug",
        "treats",
        "disease",
        "示例降糖片",
        "2型糖尿病"
      ],
      [
        "drug",
        "treats",
        "disease",
        "示例降糖片",
        "胰岛素抵抗综合征"
      ]
    ],
    "raw_data": {
      "药品名称": "示例降糖片",
      "商品名": "糖稳宁",
      "英文名": "Example Hypoglycemic Tablets",
      "成分": [
        {
          "化学名称": "盐酸二甲双胍",
          "化学式": "C4H11N5·HCl",
          "含量": "每片含500mg"
        },
        {
          "辅料": "微晶纤维素、硬脂酸镁"
        }
      ],
      "适应症": [
        "2型糖尿病",
        "胰岛素抵抗综合征"
      ],
      "用法用量": {
        "成人": "起始剂量500mg/次，每日2次，随餐服用",
        "最大剂量": "每日不超过2000mg",
        "调整原则": "根据血糖监测结果调整剂量"
      },
      "不良反应": [
        "常见：恶心、腹泻（发生率>10%）",
        "偶见：维生素B12吸收减少（发生率1-10%）",
        "罕见：乳酸酸中毒（发生率<1%）"
      ],
      "禁忌": [
        "严重肾功能不全（eGFR<30mL/min）",
        "糖尿病酮症酸中毒",
        "妊娠期妇女"
      ],
      "药物相互作用": [
        "与碘造影剂联用可能增加肾毒性",
        "增强华法林的抗凝效果"
      ],
      "贮藏": "30℃以下阴凉干燥处保存",
      "包装": "铝塑泡罩包装，30片/盒",
      "批准文号": "国药准字H20230001",
      "生产企业": "示例制药有限公司"
    }
  }
"""

class MyExtractData():
    def __init__(self):
        pass
        
    # 定义实体识别和关系抽取函数
    def extract_entities_and_relationships(self, nlp, text: str):
        # text = "Spinal and bulbar muscular atrophy (SBMA) is an \
        #    inherited motor neuron disease caused by the expansion \
        #    of a polyglutamine tract within the androgen receptor (AR). \
        #    SBMA can be caused by this easily."
        doc = nlp(text)
        spacy.displacy.render(doc, style="ent")
        entities = {}
        relationships = []

        # 提取实体
        for ent in doc.ents:
            entities[ent.text] = ent.label_

        # 简单的关系抽取示例
        print(f"doc: {doc}")
        for token in doc:
            print(
                f"""token: {token}, token.dep_: {token.dep_}, 
                token.head.text: {token.head.text}, token.head.pos_: {token.head.pos_}
                "children": {[child.text for child in token.children]}"""
            )
            if token.dep_ == 'prep' and token.head.text in entities:
                related_entity = [child for child in token.children if child.dep_ == 'pobj']
                if related_entity:
                    relationships.append((entities[token.head.text], token.head.text, entities[related_entity[0].text]))

        return entities, relationships
    
    def test(self, csv_path: str):
        # 加载spaCy模型
        # nlp = spacy.load("zh_core_web_md")
        nlp = spacy.load("zh_core_web_trf")
        # nlp = spacy.load("en_ner_bc5cdr_md")

        # 读取医学文本数据
        # "14_medical_consultation_system/data/medical_texts.csv"
        data = pd.read_csv(csv_path)
        
        # 遍历数据并提取信息
        for index, row in data.iterrows():
            text = row['text']
            entities, relationships = self.extract_entities_and_relationships(nlp, text)
            print(f"Text: {text}")
            print(f"Entities: {entities}")
            print(f"Relationships: {relationships}")
            print("\n")

    def load_icd10(self, csv_icd10_path: str):
        df = pd.read_csv(csv_icd10_path, sep='\t')
        diseases = []
        for _, row in df.iterrows():
            code = row[0].strip()
            name = re.sub(r'\(.*?\)', '', row[1]).strip()  # 清理括号内容
            diseases.append({"code": code, "name": name})
        return diseases
    
    # 非结构化文本处理（示例：药品说明书）
    def process_drug_instructions(self, text):
        patterns = {
            'drug_name': r'【药品名称】\s*(.*?)\n',
            'indications': r'【适应症】\s*(.*?)\n'
        }
        extracted = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            extracted[key] = match.group(1).strip() if match else None
        return extracted
    
    def parse_drug_manual(self, json_path: str):
        """解析药品说明书数据"""
        with open(json_path, 'r', encoding='utf-8') as f:
            drugs = json.load(f)
            
        structured_data = []
        for drug in drugs:
            # 提取关键实体
            entities = [
                ("drug", drug["药品名称"]),
                ("chemical", drug["成分"][0]["化学名称"]),
                ("company", drug["生产企业"])
            ]
            
            # 提取关系
            relations = [
                ("drug", "contains_chemical", "chemical", drug["药品名称"], drug["成分"][0]["化学名称"]),
                ("drug", "produced_by", "company", drug["药品名称"], drug["生产企业"])
            ]
            
            # 疾病关联
            for indication in drug["适应症"]:
                entities.append( ("disease", indication) )
                relations.append( ("drug", "treats", "disease", drug["药品名称"], indication) )
            
            structured_data.append({
                "entities": entities,
                "relations": relations,
                "raw_data": drug
            })
        return structured_data
    
    def build_drug_kg(self, data):
        g = Graph("bolt://localhost:7687", auth=("neo4j", "0123456789"))
        
        for item in data:
            # 创建实体节点
            for entity in item["entities"]:
                node = Node(entity[0], name=entity[1])
                g.merge(node, entity[0], "name")
                
            # 创建关系
            for rel in item["relations"]:
                query = f"""
                MATCH (a:{rel[0]} {{name: $a_name}}), (b:{rel[2]} {{name: $b_name}})
                MERGE (a)-[:{rel[1]}]->(b)
                """
                g.run(query, a_name=rel[3], b_name=rel[4])

def test_spacy(my_extract_data: MyExtractData):
    csv_path = "14_medical_consultation_system/data/medical_texts.csv"
    my_extract_data.test(csv_path)
    
def test_load_icd10(my_extract_data: MyExtractData):
    csv_icd10_path = "14_medical_consultation_system/data/01_structured_data/disease.csv"
    my_extract_data.load_icd10(csv_icd10_path)
    
def test_build_drug_kg(my_extract_data: MyExtractData):
    json_path = "14_medical_consultation_system/data/02_nstructured_data/drug_instructions.json"
    result = my_extract_data.parse_drug_manual(json_path)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    my_extract_data.build_drug_kg(result)
    

if __name__ == "__main__":
    my_extract_data = MyExtractData()
    
    test_spacy(my_extract_data)

