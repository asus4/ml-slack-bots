import argparse
import base64
import json
from urllib import response
import requests
from huggingface_hub.inference_api import InferenceApi

from . import Config


# inference = InferenceApi(repo_id="bert-base-uncased", token=Config.HUGGINGFACE_API_TOKEN)
# print(inference)


def distilbert_base_uncased(payload):
    headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"}
    API_URL = f"https://api-inference.huggingface.co/models/distilbert-base-uncased"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def dallemini(prompt):
    headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"}
    API_URL = f"https://hf.space/embed/eetn/DALL-E/+/api/predict/"
    json = {"data": [prompt]}
    response = requests.post(API_URL, headers=headers, json=json)
    print(response)
    return response.json()


def latent_diffusion(
    prompt: str,
    steps=50,
    width=256,
    height=256,
    images=2,
    diversity_scale=5,
    mock=False,
):
    """
    latent diffusion model
    https://hf.space/embed/multimodalart/latentdiffusion/api
    """

    res = None

    if mock:
        res = mock_response("test/latent_diffusion.json")
    else:
        response = requests.post(
            url="https://hf.space/embed/multimodalart/latentdiffusion/+/api/predict/",
            headers={"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"},
            json={
                "data": [
                    prompt,
                    steps,
                    str(width),
                    str(height),
                    images,
                    diversity_scale,
                ]
            },
        )
        res = response.json()
        print(f"latent_diffusion json: {json.dumps(res)}")

        # for debug
        # save_response(response, "test/latent_diffusion.json")

    return find_images(res["data"][1])


def save_response(response, filename):
    with open(filename, "wb") as f:
        f.write(response.content)


def mock_response(filename: str):
    with open(filename, "r") as f:
        return json.load(f)


def find_images(obj):
    images = []

    if type(obj) is dict:
        for _, value in obj.items():
            images.extend(find_images(value))
    elif type(obj) is list:
        for item in obj:
            images.extend(find_images(item))
    elif type(obj) is str:
        # Decode base64 to png binary
        if obj.startswith("data:image/png;base64,"):
            txt = obj.replace("data:image/png;base64,", "")
            images.append(base64.b64decode(txt, validate=True))
    return images


if __name__ == "__main__":
    """
    Local test with
    python -m app.text2image --json test/latent_diffusion.json
    """
    parser = argparse.ArgumentParser(description="Test Lambda Function locally")
    parser.add_argument("--json", type=str, help="Test data in JSON format")
    args = parser.parse_args()

    images = []
    with open(args.json, "r", encoding="utf-8") as f:
        response = json.load(f)
        images.extend(find_images(response["data"][1]))

    for index, image in enumerate(images):
        with open(f"test/image{index}.png", "wb") as f:
            f.write(image)
    print(f"Saved {len(images)} images")
