## **Installation**

```
sudo apt-get update
sudo apt-get install poppler-utils ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools

conda create -n olmocr python=3.11
conda activate olmocr

git clone https://github.com/allenai/olmocr.git
cd olmocr
pip install -e .

pip install sgl-kernel==0.0.3.post1 --force-reinstall --no-deps
pip install "sglang[all]==0.4.2" --find-links https://flashinfer.ai/whl/cu124/torch2.4/flashinfer/ 

huggingface-cli download allenai/olmOCR-7B-0225-preview --max-workers 1 --local-dir save-path
```

## **Test**
```
python -m olmocr.pipeline ./localworkspace --pdfs tests/gnarly_pdfs/horribleocr.pdf --model save-path
```