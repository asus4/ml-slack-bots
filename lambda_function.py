import os
import requests
from huggingface_hub.inference_api import InferenceApi

HUGGINGFACE_API_TOKEN = os.environ['HUGGINGFACE_API_TOKEN']

inference = InferenceApi(repo_id="bert-base-uncased", token=HUGGINGFACE_API_TOKEN)
print(inference)

def distilbert_base_uncased(payload):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    API_URL = f"https://api-inference.huggingface.co/models/distilbert-base-uncased"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def dallemini(prompt):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    API_URL = f"https://hf.space/embed/eetn/DALL-E/+/api/predict/"
    json = {
        "data": [ prompt ]
    }
    response = requests.post(API_URL, headers=headers, json=json)
    print(response)
    return response.json()

def latentdiffusion(prompt):
    headers = {
        # "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    API_URL = f"https://hf.space/embed/multimodalart/latentdiffusion/+/api/predict/"
    json = {
        "data": [ prompt, 50, "128", "128", 2 , 5 ]
    }
    response = requests.post(API_URL, headers=headers, json=json)
    return response.json()

def lambda_handler(event, context):   
    response = requests.get("https://www.google.com/")
    print(response.text)
    return response.text

if __name__ == '__main__':
    print(HUGGINGFACE_API_TOKEN)
    
    # data = distilbert_base_uncased("The goal of life is [MASK].")
    # print(data)

    data = dallemini("sunset over a lake in the mountains")
    print(data)

    # data = latentdiffusion("sunset over a lake in the mountains")
    # print(data)

    # result = lambda_handler(None, None)
    # print(result)
