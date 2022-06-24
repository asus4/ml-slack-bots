import os
import requests

HUGGINGFACE_API_TOKEN = os.environ['HUGGINGFACE_API_TOKEN']

def distilbert_base_uncased(payload):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    API_URL = f"https://api-inference.huggingface.co/models/distilbert-base-uncased"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def lambda_handler(event, context):   
    response = requests.get("https://www.google.com/")
    print(response.text)
    return response.text

if __name__ == '__main__':
    print(HUGGINGFACE_API_TOKEN)
    data = distilbert_base_uncased("The goal of life is [MASK].")
    print(data)
    # result = lambda_handler(None, None)
    # print(result)
