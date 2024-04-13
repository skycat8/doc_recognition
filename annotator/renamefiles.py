import os
import hashlib
from argparse import ArgumentParser
from shutil import move

import cv2
from tqdm import tqdm

ap = ArgumentParser("")
ap.add_argument("--path", default=None, help="path to local directory")
args = ap.parse_args()

if args.path is None:
    print(f"--path argument should not be empty! Abort...")
    exit(1)
elif not os.path.exists(args.path):
    print(f"Path '{args.path}' does not exist! Abort...")
    exit(2)


def less_than(filename, max_bytes=3.0E6):
    size_bytes = os.stat(filename).st_size
    if size_bytes < max_bytes:
        return True
    return False


def isimage(filename):
    parts = filename.rsplit('.', 1)
    if len(parts) == 1:
        return False
    if parts[1].lower() in ['jpg', 'jpeg', 'png']:
        return True
    return False


for subdir in [s.name for s in os.scandir(args.path) if s.is_dir()]:
    subdir = os.path.join(args.path, subdir)
    print(f"'{subdir}' progress:")
    for filename in tqdm([f.name for f in os.scandir(subdir) if f.is_file() and isimage(f.name)]):
        parts = filename.rsplit('.',1)
        target_name = None
        if len(parts) == 2:
            extension = parts[1].lower()
            if extension == 'jpeg':
                extension = 'jpg'
            target_name = hashlib.sha1(parts[0].encode('utf-8')).hexdigest()[:11] + '.' + extension
        elif len(parts) == 1:
            target_name = hashlib.sha1(parts[0].encode('utf-8')).hexdigest()[:11] + '.jpg'
        if target_name:
            target_name = os.path.join(subdir, target_name)
            source_name = os.path.join(subdir, filename)
            exceeds_api_size_limit = not less_than(os.path.join(subdir, filename))
            if exceeds_api_size_limit:
                mat = cv2.imread(source_name, cv2.IMREAD_COLOR)
                mat = cv2.resize(mat, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                cv2.imwrite(target_name, mat)
                os.remove(source_name)
            else:
                move(source_name, target_name)