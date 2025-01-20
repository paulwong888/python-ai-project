#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate torch231
# pip list
pip install lmms_eval --no-input
pip install librosa --no-input



# tail -f awq_w_only.log
#conda activate torch231
#You can use pip list in the container to check the packages installed.
#You can find calib/eval datasets at /home/datasets/llmc.zip
#cd /home/datasets
#unzip llmc.zip
