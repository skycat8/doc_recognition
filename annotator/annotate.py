import asyncio
import os
import json
from claude3 import get_antropic_client_session, annotete_by_claude
from tqdm import tqdm
from datamodels import pass_schema, pts_schema, sts_schema, drivings_schema
from argparse import ArgumentParser
import json_repair

ap = ArgumentParser("")
ap.add_argument("--path", default=None, help="path to local directory")
args = ap.parse_args()

if args.path is None:
    print(f"--path argument should not be empty! Abort...")
    exit(1)
elif not os.path.exists(args.path):
    print(f"Path '{args.path}' does not exist! Abort...")
    exit(2)


def isimage(filename):
    parts = filename.rsplit('.', 1)
    if len(parts) == 1:
        return False
    if parts[1].lower() in ['jpg', 'jpeg', 'png']:
        return True
    return False


def less_than(filename, max_bytes=3.8E6):
    size_bytes = os.stat(filename).st_size
    if size_bytes < max_bytes:
        return True
    return False


async def main():
    client_session = await get_antropic_client_session()

    documents = {
        'pts': pts_schema,
        'sts': sts_schema,
        'pass': pass_schema,
        'drivings': drivings_schema,
    }

    for key in documents:
        if documents[key] is not None:
            print(f"ANNOTATING SAMPLES FOR CLASS: {key}")
            path = f"{args.path}/{key}"
            files_list = [os.path.join(path, f.name) for f in os.scandir(path) if
                          (f.is_file() and isimage(f.name) and less_than(os.path.join(path, f.name)))]
            for filename in tqdm(files_list):
                json_filename = filename.rsplit('.', 1)[0] + '.json'
                if os.path.exists(json_filename):
                    continue
                status, reply = await annotete_by_claude(filename, client_session, documents[key])
                annotation = None
                if status == 200:
                    try:
                        full_text = reply['content'][0]['text']
                        start = full_text.find('{')
                        stop = full_text.rfind('}') + 1
                        annotation = json_repair.loads(full_text[start:stop])
                    except Exception as ex:
                        print(ex, reply['content'][0]['text'])
                        annotation = None
                if annotation:
                    if key == 'drivings':
                        if ((annotation['first_name_ru'] == '-' or annotation['last_name_ru'] == '-') and
                                annotation['experience'] != '-'):
                            annotation['pages'] = [2]
                    elif key == 'sts':
                        if ((annotation['first_name_ru'] == '-' or annotation['last_name_ru'] == '-') and
                                (annotation['regid'] != '-' or annotation['color'] != '-')):
                            annotation['pages'] = [2]
                    with open(json_filename, 'w') as o_f:
                        o_f.write(json.dumps(annotation, separators=(',', ':'), indent=4, ensure_ascii=False))

    await client_session.close()


if __name__ == "__main__":
    asyncio.run(main())
