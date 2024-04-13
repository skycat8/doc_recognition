import os
import json
import numpy
import cv2
from tqdm import tqdm
import random
from argparse import ArgumentParser
from shutil import copy
import albumentations as A

ap = ArgumentParser("")
ap.add_argument("--path", default=None, help="path to local directory")
ap.add_argument("--out", default=None, help="path to output directory")
ap.add_argument("--max_samples_per_class", default=500, help="max samples per class")
ap.add_argument("--augment", default=4, type=int, help="how many augmented samples to make per sample")
args = ap.parse_args()

if args.path is None:
    print(f"--path argument should not be empty! Abort...")
    exit(1)
elif not os.path.exists(args.path):
    print(f"Path '{args.path}' does not exist! Abort...")
    exit(2)
if args.out is None:
    print(f"--out argument should not be empty! Abort...")
    exit(3)
elif not os.path.exists(args.out):
    os.makedirs(args.out, exist_ok=True)
    if not os.path.exists(args.out):
        print(f"Path '{args.out}' can not be created! Abort...")
        exit(4)

if args.augment > 0:
    transforms = A.Compose([
        A.Transpose(p=0.25),
        A.RandomBrightnessContrast(p=0.25, brightness_limit=(-0.25, 0.25)),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.SafeRotate(p=1.0, limit=(-45, 45), border_mode=cv2.BORDER_CONSTANT),
        A.GaussNoise(p=0.5, var_limit=(1, 35)),
        A.MotionBlur(p=0.5, blur_limit=11),
        A.ImageCompression(p=0.25, quality_lower=70, quality_upper=100),
        A.RandomBrightnessContrast(p=0.25, brightness_limit=(-0.25, 0.25)),
        A.ToGray(p=0.25),
        A.ColorJitter(p=0.5),
    ], p=1.0)


def create_llava_markup_instance(_id: int, _filename: str, _target: str):
    human = random.choice([
        'Convert to json with document attributes.',
        'What do yo see on picture?',
        'Describe what you see on document scan.',
        'Extract information about person from the given photo.',
        'Extract information from the given photo of document.',
        'Reply with information from document in json',
        'Who is the owner of the document?'
        "What document attributes do you see?"
    ])
    out = {
        'id': f"identity_{_id}",
        'conversations': [
            {'from': 'user',
             'value': f'Picture 1: <img>{_filename}</img>\n{human}'},
            {'from': 'assistant',
             'value': _target}
        ]
    }
    return out


targetdirectory = args.out.rsplit('/', 1)[1]

num = 0
num_unique = {}
data_samples = []

for subdir in [s.name for s in os.scandir(args.path) if s.is_dir()]:
    abs_subdir_src = os.path.join(args.path, subdir)
    abs_subdir_target = os.path.join(args.out, subdir)
    if not os.path.exists(abs_subdir_target):
        os.makedirs(abs_subdir_target)
    print(f"'{subdir}' progress:")
    num_unique[subdir] = 0
    files_list = [f.name for f in os.scandir(abs_subdir_src) if f.is_file() and '.json' not in f.name]
    random.shuffle(files_list)
    files_list = files_list[:args.max_samples_per_class]
    for filename in tqdm(files_list):
        sample = None
        img_filename = os.path.join(abs_subdir_src, filename)
        json_filename = img_filename.rsplit('.', 1)[0] + '.json'
        if os.path.exists(json_filename):
            with open(json_filename, 'r') as i_f:
                sample = json.load(i_f)
        if sample:
            copy(img_filename, os.path.join(abs_subdir_target, filename))
            markup = create_llava_markup_instance(num,
                                                  os.path.join(targetdirectory, subdir, filename),
                                                  json.dumps(sample,
                                                             separators=(',', ':'),
                                                             ensure_ascii=False))
            data_samples.append(markup)
            num += 1
            num_unique[subdir] += 1
            if args.augment > 0:
                mat = cv2.imread(img_filename, cv2.IMREAD_COLOR)
                for i in range(args.augment):
                    new_filename = filename.rsplit('.', 1)[0] + f"_{i}.jpg"
                    new_abs_filename = os.path.join(targetdirectory, abs_subdir_target, new_filename)
                    variant = transforms(image=mat)["image"]
                    cv2.imwrite(new_abs_filename, variant)
                    markup = create_llava_markup_instance(num,
                                                          os.path.join(targetdirectory, subdir, new_filename),
                                                          json.dumps(sample,
                                                                     separators=(',', ':'),
                                                                     ensure_ascii=False))
                    data_samples.append(markup)
                    num += 1


with open(os.path.join(args.out, 'for_qwen.json'), 'w') as o_f:
    json.dump(data_samples, o_f, separators=(',', ':'), ensure_ascii=False, indent=4)

print(f"TOTAL SAMPLES: {num}")
print("UNIQUE:")
for key in num_unique:
    print(f" - {key}: {num_unique[key]}")
