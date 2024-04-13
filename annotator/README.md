Auto annotator
===

1. Prepare folder with photos of a documents on local disk;
2. Get Antropic API access;
3. Run annotation;
4. Check annotation manually;
5. Create json for VL-LM finetuning.

## Installation

```bash
pip install -r requirements.txt --no-cache-dir
```

## Run annotation

```bash
python -m renamefiles --path "/local/path/to/photos"  # rename files, resize heavy photos 
python -m annotate --path "/local/path/to/photos"  # make auto annotation for photos
```

## Run markup creation (model format specific) with optional augmentation

for LlaVa

```bash
python -m llava --path "/local/path/to/photos" --out "/local/path/to/train" --augment 3  
```

for Qwen-VL

```bash
python -m qwen --path "/local/path/to/photos" --out "/local/path/to/train" --augment 3
```



