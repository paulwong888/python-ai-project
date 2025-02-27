docker compose down
docker compose up -d
# docker compose exec my-service "ls -l"
docker exec -it llmc /bin/bash
# docker exec -it llmc source /root/miniconda3/bin/activate && "/root/miniconda3/bin/conda activate torch231"

#conda activate torch231
#You can use pip list in the container to check the packages installed.
#You can find calib/eval datasets at /home/datasets/llmc.zip
#cd /home/datasets
#unzip llmc.zip
