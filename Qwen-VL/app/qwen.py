import json
import cv2
import os
import uuid
import re
from modelscope import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model_tokenizer(base_model='Qwen/Qwen-VL-Chat-Int4',
                         qlora_path='/home/sasha/Programming/gagarin/Qwen-VL/output_qwen_0'):
    tokenizer = AutoTokenizer.from_pretrained(
        base_model,
        trust_remote_code=True, resume_download=True, revision='master',
    )
    model = AutoModelForCausalLM.from_pretrained(
        qlora_path,  # path to the output directory
        device_map=("cuda" if torch.cuda.is_available() else "cpu"),
        trust_remote_code=True,
        revision="master",
    ).eval()
    model.generation_config = GenerationConfig.from_pretrained(
        base_model,
        trust_remote_code=True, resume_download=True, revision='master',
    )
    return tokenizer, model


def _parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split("`")
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f"<br></code></pre>"
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", r"\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def _remove_image_special(text):
    text = text.replace('<ref>', '').replace('</ref>', '')
    return re.sub(r'<box>.*?(</box>|$)', '', text)


def predict(tokenizer, model, image):
    filename = uuid.uuid4().hex + '.jpg'
    cv2.imwrite(filename, image)
    query = "Extract information about person from the given photo."
    message = f"Picture 1: <img>{filename}</img>\n{query}"
    for response in model.chat_stream(tokenizer, message, history=[]):
        response = _remove_image_special(_parse_text(response))
    os.remove(filename)
    json_response = {}
    try:
        json_response = json.loads(response)
    except Exception as ex:
        print(f"EXCEPTION >> {ex}")
    return json_response, response


def test(tokenizer, model):
    photo = cv2.imread("./app/res/drivings.jpg", cv2.IMREAD_COLOR)
    return predict(tokenizer, model, photo)
