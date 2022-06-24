import requests

from . import Config

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
