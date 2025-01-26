docker compose start llmc
docker exec -it llmc /bin/bash

#conda activate torch231
#You can use pip list in the container to check the packages installed.
#You can find calib/eval datasets at /home/datasets/llmc.zip
#cd /home/datasets
#unzip llmc.zip
