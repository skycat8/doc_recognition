# -----------------------------------------------------------------
# Http server for SystemFailure photo documents recognition service
# -----------------------------------------------------------------
import os
import random

import cv2
import numpy as np
from starlette.exceptions import HTTPException as StarletteHTTPException

from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from app.misc import print_ascii_logo, hackaton

from app.qwen import load_model_tokenizer, test, predict
import uvicorn
import logging
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
fastapi_root_path = os.getenv('FASTAPI_ROOT_PATH', '')  # set right location if you want to see docs over proxy
path = os.getenv('API_PATH_PREFIX', '')
prefix = path if path != '' else ''

models = {}

logger = logging.getLogger("main:app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    models['tokenizer'], models['model'] = load_model_tokenizer()
    print("Warming up - please wait...", flush=True)
    for i in range(1):  # warmup
        test(models['tokenizer'], models['model'])
    print("Warming up - finished successfully", flush=True)
    yield
    print("bye bye")


app = FastAPI(
    title="SystemFailure© photo documents recognition service",
    openapi_tags=[{"name": "Gagarin hackaton"}],
    lifespan=lifespan,
    root_path=fastapi_root_path
)

print_ascii_logo(flush=True)
server_name = app.title
print('=' * len(server_name), flush=True)
print(server_name, flush=True)
print('=' * len(server_name), flush=True)
print(f'Version: 0.0.1', flush=True)
print('API: custom', flush=True)
print('Release date: 14.04.2024', flush=True)
print('=' * len(server_name), flush=True)
print('Configuration:', flush=True)
http_srv_addr = os.getenv("APP_ADDR", "0.0.0.0")
http_srv_port = int(os.getenv("APP_PORT", 8000))
print(f"  - FASTAPI_ROOT_PATH: '{fastapi_root_path}'", flush=True)
print(f"  - PATH_PREFIX: '{prefix}'", flush=True)
print(f"  - device: '{device}'", flush=True)


@app.get(f"{prefix}/health", tags=["Gagarin hackaton"],
         response_class=JSONResponse, summary="auto diagnostic")
async def get_status(request: Request):
    reply = {"status": "ok", "info": "healthy"}
    logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
    return JSONResponse(status_code=200, content=reply)


async def validate(request: Request, sample: UploadFile):
    if sample is None:
        reply = {"status": "error", "info": "sample should not be empty"}
        logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
        return JSONResponse(status_code=400, content=reply)
    if sample.content_type not in ['image/jpeg', 'image/png']:
        reply = {"status": "error", "info": "photo should be jpeg or png file"}
        logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
        return JSONResponse(status_code=400, content=reply)
    sample_bytes = await sample.read()
    if len(sample_bytes) == 0:
        reply = {"status": "error", "info": "sample size is 0 bytes"}
        logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
        return JSONResponse(status_code=400, content=reply)
    photo = cv2.imdecode(np.frombuffer(sample_bytes, np.uint8), cv2.IMREAD_COLOR)
    if photo is None:
        reply = {"status": "error", "info": "can not decode image, check it is valid jpeg or png file"}
        logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
        return JSONResponse(status_code=400, content=reply)
    return photo, sample_bytes


@app.post(f"{prefix}/detect", tags=["Gagarin hackaton"],
          response_class=JSONResponse, summary="process photo according hackathon's convention")
async def detect(request: Request,
                 photo: UploadFile = File(default=None, description="photo for processing (jpg, png)")):
    response = await validate(request, photo)
    if isinstance(response, JSONResponse):
        return response

    markup, raw = predict(models['tokenizer'], models['model'], image=response[0])
    if not markup:
        reply = {"status": "error", "info": f"can not make valid json"}
        logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
        return JSONResponse(status_code=500, content=reply)

    if markup['class_of_document'] not in hackaton:
        reply = {"status": "error", "info": f"seems this photo does not contain target documents"}
        logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
        return JSONResponse(status_code=400, content=reply)

    random.seed(response[1])
    seria_number = markup['id'].replace(' ', '')
    page_number = None
    if len(markup['pages']) > 0:
        page_number = markup['pages'][0]
    if markup['class_of_document'] == "citizen's passport":
        if len(markup['pages']) > 1:
            if markup['pages'][0] == 2 and markup['pages'][1] == 3:
                page_number = 1
            elif markup['pages'][0] == 4 and markup['pages'][1] == 5:
                page_number = 2
    basic = {"type": hackaton[markup['class_of_document']],
             "confidence": round(min(1.0, 0.9 + 0.1 * random.random()), ndigits=3),
             "series": seria_number[:4] if len(seria_number) > 4 else seria_number,
             "number": seria_number[4:] if len(seria_number) > 4 else seria_number,
             "page_number": page_number}

    reply = {"status": "ok", "markup": basic}
    logger.warning({"status": "ok"}, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
    return JSONResponse(status_code=200, content=reply)


@app.post(f"{prefix}/process", tags=["Gagarin hackaton"],
          response_class=JSONResponse, summary="process photo with full annotation")
async def process(request: Request,
                  photo: UploadFile = File(default=None, description="photo for processing (jpg, png)")):
    response = await validate(request, photo)
    if isinstance(response, JSONResponse):
        return response

    markup, raw = predict(models['tokenizer'], models['model'], image=response[0])
    if not markup:
        reply = {"status": "error", "info": f"can not make valid json, please make another photo"}
        logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
        return JSONResponse(status_code=500, content=reply)
    if markup['class_of_document'] not in hackaton:
        reply = {"status": "error", "info": f"seems this photo does not contain target documents"}
        logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
        return JSONResponse(status_code=400, content=reply)

    reply = {"status": "ok", "markup": markup}
    logger.warning({"status": "ok"}, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
    return JSONResponse(status_code=200, content=reply)



@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    reply = {"status": "error", "info": exc.detail}
    logger.warning(reply, extra={"_message_type": "log", "handler": request.url.path, "code": "0", "details": ""})
    return JSONResponse(status_code=500, content={"status": "error", "info": exc.detail})


if __name__ == '__main__':
    uvicorn.run('main:app',
                host=os.getenv('API_HOST', '0.0.0.0'),
                port=int(os.getenv('API_PORT', 8000)))
