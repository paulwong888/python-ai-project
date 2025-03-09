import json, torch
from transformers import (
    AutoConfig,
    AutoTokenizer,
    AutoModelForCausalLM,
    GenerationConfig,
)
from peft import PeftModel
from transformers import BitsAndBytesConfig
from a04_0_constant import *



# task = 'NER'
# language = 'en'
# schema = ['person', 'organization', 'else', 'location']
# input = '284 Robert Allenby ( Australia ) 69 71 71 73 , Miguel Angel Martin ( Spain ) 75 70 71 68 ( Allenby won at first play-off hole )'











# sintruct = "{\"instruction\": \"You are an expert in named entity recognition. Please extract entities that match the schema definition from the input. Return an empty list if the entity type does not exist. Please respond in the format of a JSON string.\", \"schema\": [\"person\", \"organization\", \"else\", \"location\"], \"input\": \"284 Robert Allenby ( Australia ) 69 71 71 73 , Miguel Angel Martin ( Spain ) 75 70 71 68 ( Allenby won at first play-off hole )\"}"
# sintruct = '<reserved_106>' + sintruct + '<reserved_107>'
# input_ids = tokenizer.encode(sintruct, return_tensors="pt").to(device)


class MyRelationExtraModel():
    def __init__(self):
        # model_root_path = "/home/paul/.cache/huggingface/hub/combine-models/medical/extract-relation/"
        # model_path = model_root_path + "models--baichuan-inc--Baichuan2-13B-Chat/"
        # lora_path = model_root_path + "models--zjunlp--baichuan2-13b-iepile-lora/"

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # model_path = "baichuan-inc/Baichuan2-13B-Chat"
        # lora_path = "zjunlp/baichuan2-13b-iepile-lora"

        config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

        # model = AutoModelForCausalLM.from_pretrained(
        #     model_path,
        #     config=config,
        #     device_map="auto",  
        #     torch_dtype=torch.bfloat16,
        #     trust_remote_code=True,
        #     offload_folder="./offload",  # 关键参数：自定义分载目录
        #     use_safetensors=False
        # )


        # model = PeftModel.from_pretrained(
        #     model,
        #     lora_path,
        # )


        quantization_config=BitsAndBytesConfig(     
            load_in_4bit=True,
            llm_int8_threshold=6.0,
            llm_int8_has_fp16_weight=False,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            config=config,
            device_map="auto", 
            quantization_config=quantization_config,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )

        self.model = PeftModel.from_pretrained(
            model,
            lora_path,
        )

        self.model.eval()

    def build_prompt(self, task: str, language: str, schema: list[str], input: str) -> list[str]:
        split_num = split_num_mapper[task]
        split_schemas = [schema[i:i+split_num] for i in range(0, len(schema), split_num)]
        sintructs = []
        for split_schema in split_schemas:
            sintruct = json.dumps({'instruction':instruction_mapper[task+language], 'schema':split_schema, 'input':input}, ensure_ascii=False)
            sintruct = '<reserved_106>' + sintruct + '<reserved_107>'
            sintructs.append(sintruct)
        
        return sintructs

    def generate(self, task: str, language: str, schema: list[str], input: str) -> str:
        sintructs = self.build_prompt(task, language, schema, input)
        input_ids = self.tokenizer.encode(sintructs[0], return_tensors="pt").to(self.device)

        input_length = input_ids.size(1)
        generation_output = self.model.generate(
            input_ids=input_ids, 
            generation_config=GenerationConfig(max_length=512, max_new_tokens=256, return_dict_in_generate=True)
        )
        generation_output = generation_output.sequences[0]
        generation_output = generation_output[input_length:]
        output = self.tokenizer.decode(generation_output, skip_special_tokens=True)

        return output

if __name__ == "__main__":
    my_relation_extra_model = MyRelationExtraModel()

    task = 'RE'
    language = 'zh'
    schema = ['同义词（疾病）', '内窥镜检查', '病理分型', '临床表现']
    input = "4.十二指肠炎（duodenitis） 十二指肠炎常多相伴其他部位的炎症，内镜下黏膜炎症的改变有四种类型： （1）充血型： 黏膜充血、水肿，镜下反光增强。 （4）出血糜烂型： 黏膜充血处见点状、片状或蜂窝状糜烂，表面可有出血。"

    print(my_relation_extra_model.generate(task, language, schema, input))

    schema = ['疾病_药物治疗_药物']
    input = "患者有高血压和糖尿病，建议使用洛卡特普和二甲双胍。"
    print(my_relation_extra_model.generate(task, language, schema, input))
