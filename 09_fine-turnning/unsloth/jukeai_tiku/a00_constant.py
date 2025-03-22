import torch, os
from unsloth import is_bfloat16_supported
from dotenv import load_dotenv
from a00_basic_constant import *

load_dotenv("/home/paul/paulwong/work/config")
fp16=not is_bfloat16_supported()
bf16=is_bfloat16_supported()