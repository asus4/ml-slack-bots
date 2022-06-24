import requests
from huggingface_hub.inference_api import InferenceApi

from . import Config


# inference = InferenceApi(repo_id="bert-base-uncased", token=Config.HUGGINGFACE_API_TOKEN)
# print(inference)

def distilbert_base_uncased(payload):
    headers = {
        "Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"
    }
    API_URL = f"https://api-inference.huggingface.co/models/distilbert-base-uncased"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def dallemini(prompt):
    headers = {
        "Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"
    }
    API_URL = f"https://hf.space/embed/eetn/DALL-E/+/api/predict/"
    json = {
        "data": [ prompt ]
    }
    response = requests.post(API_URL, headers=headers, json=json)
    print(response)
    return response.json()


def latent_diffusion(prompt):
    response = requests.post(
        url = "https://hf.space/embed/multimodalart/latentdiffusion/+/api/predict/",
        headers = {
            "Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"
        },
        json = {
            "data": [ prompt, 50, "128", "128", 2 , 5 ]
        }
    )
    return response.json()
