import argparse
import base64
import json
import replicate
import requests
from huggingface_hub.inference_api import InferenceApi

from . import Config


def distilbert_base_uncased(payload):
    headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"}
    API_URL = f"https://api-inference.huggingface.co/models/distilbert-base-uncased"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def dalle_mini(prompt: str, n_predictions=2, mock=False):
    """
    Dalle Mini model
    https://replicate.com/borisdayma/dalle-mini
    """

    response = None

    if mock:
        response = mock_response("test/dalle_mini.json")
    else:
        print(f"prompt: {prompt}")
        model = replicate.models.get("borisdayma/dalle-mini")
        results = model.predict(
            prompt=prompt,
            n_predictions=n_predictions,
        )

        print(f"dalle_mini results: {results}")
        response = list((result["image"] for result in results))
    return response


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

    response = None

    if mock:
        response = mock_response("test/latent_diffusion.json")
    else:
        res = requests.post(
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
        response = res.json()
        print(f"latent_diffusion json: {json.dumps(response)}")

        # for debug
        # save_response(res, "test/latent_diffusion.json")

    return find_images(response["data"][1])


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

    res = dalle_mini("An astronaut riding a horse in a photorealistic style")
    print(res)
