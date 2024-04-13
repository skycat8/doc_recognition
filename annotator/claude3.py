import asyncio
import json
import aiohttp
from config import cfg
import base64
from datamodels import pass_schema, drivings_schema, pts_schema, sts_schema


async def get_antropic_client_session():
    return aiohttp.ClientSession(base_url=cfg['ANTRROPIC_BASE_URL'],
                                    headers={'x-api-key': cfg['ANTROPIC_API_KEY'],
                                             'anthropic-version': cfg['ANTROPIC_API_VERSION']})


async def annotete_by_claude(filename, client_session, document_schema, max_tokens=2000, model=cfg['ANTROPIC_MODEL_NAME']):
    endpoint = '/v1/messages'

    with open(filename, 'rb') as i_f:
        binary_data = i_f.read()

    payload = {'model': model, 'max_tokens': max_tokens, 'messages': [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": 'image/jpeg' if '.jp' in filename.lower() else 'image/png',
                        "data": base64.b64encode(binary_data).decode("utf-8")
                    },
                },
                {
                    "type": "text",
                    "text": f"Oh, I finally found you. There is no time to explain, I need your help. "
                            f"A very important person was lost. To find it you need to read the data in this photo."
                            f"Reply by json object with following schema:\n\n{document_schema}\n\n"
                            f"Be very accurate and double check what you see as life of a person is at stake. "
                            f"For all unknown and unclear values use '-' as substitution."
                }
            ],
        }
    ]}

    status, reply = None, None
    try:
        async with client_session.post(url=endpoint, json=payload) as response:
            body = await response.read()
            status = response.status
            reply = json.loads(body.decode('utf-8'))
            if response.status == 200:
                print(f'{response.method} {endpoint} - [{response.status}] - ...')
            else:
                print(f'{response.method} {endpoint} - [{response.status}] - {body}')
    except aiohttp.client_exceptions.ClientConnectorError as ex:
        print(f"{response.method} {endpoint} - [N/A] - connection error {ex}")
    return status, reply


async def bbox_by_claude(filename, client_session, document_schema, max_tokens=512, model=cfg['ANTROPIC_MODEL_NAME']):
    endpoint = '/v1/messages'

    with open(filename, 'rb') as i_f:
        binary_data = i_f.read()

    payload = {'model': model, 'max_tokens': max_tokens, 'messages': [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": 'image/jpeg' if '.jp' in filename.lower() else 'image/png',
                        "data": base64.b64encode(binary_data).decode("utf-8")
                    },
                },
                {
                    "type": "text",
                    "text": f"Give me relative bounding box coordinates of the document on photo"
                }
            ],
        }
    ]}

    status, reply = None, None
    try:
        async with client_session.post(url=endpoint, json=payload) as response:
            body = await response.read()
            status = response.status
            reply = json.loads(body)
            if response.status == 200:
                print(f'{response.method} {endpoint} - [{response.status}] - ...')
            else:
                print(f'{response.method} {endpoint} - [{response.status}] - {body}')
    except aiohttp.client_exceptions.ClientConnectorError as ex:
        print(f"{response.method} {endpoint} - [N/A] - connection error {ex}")
    return status, reply


async def main():
    client_session = await get_antropic_client_session()

    #status, reply = await bbox_by_claude('/home/alex/Testdata/gagarinhack/drivings/IMG_6263.PNG',
    #                                         client_session, pass_schema)
    #print(status, reply['content'][0]['text'])
    #exit()

    status, reply = await annotete_by_claude('/home/alex/Testdata/gagarinhack/drivings/cd4ff205920.jpg',
                                             client_session, drivings_schema)
    print(status, json.dumps(json.loads(reply['content'][0]['text']), indent=4, ensure_ascii=False))
    await client_session.close()


if __name__ == "__main__":
    asyncio.run(main())
