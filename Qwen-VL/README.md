Qwen-VL
===

Awesome fusion of LLM and ViT. Basically we have finetuned Qwen-VL-Chat-Int4 by means of QLoRa.
Single Nvidia GPU with 24G of vRAM is enough for training.


## Installation

Step 1 - install original [Qwen-VL](https://github.com/QwenLM/Qwen-VL)

```bash
git clone https://github.com/QwenLM/Qwen-VL.git
...
```

Step 2 - copy and install app

```bash
cp app Qwen-VL
pip install -r app/requirements.txt
```

## Run

```bash
uvicorn -m app.main:app --host 127.0.0.1 --port 8000
```

