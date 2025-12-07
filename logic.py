import json
import time
import requests
from config import API_IMAGE, SECRET_IMAGE
import base64
from PIL import Image
from io import BytesIO

class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline_id, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline_id),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']
    
    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)

def convert_base64_to_jpg(base64_str, output_path):
    """
    Конвертирует изображение из формата Base64 в JPG и сохраняет его.

    :param base64_str: Строка Base64, представляющая изображение.
    :param output_path: Путь для сохранения выходного файла JPG.
    """
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))
    image = image.convert("RGB")  # Конвертируем изображение в RGB
    image.save(output_path, "JPEG")

if __name__ == '__main__':
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_IMAGE, SECRET_IMAGE)
    pipeline_id = api.get_pipeline()
    uuid = api.generate("", pipeline_id)
    files = api.check_generation(uuid)
    print(files)
    if files:
        base64_image = files[0]  
        output_path = 'output_image.jpg'  
        convert_base64_to_jpg(base64_image, output_path)
        print(f"Image saved to {output_path}")
    else:
        print("No images generated.")


#Не забудьте указать именно ваш YOUR_KEY и YOUR_SECRET.