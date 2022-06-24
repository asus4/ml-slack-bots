import json
import logging

from app.text2image import latent_diffusion

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def respond(err, res=None):
    ret = {
        'statusCode': '200',
        'body': json.dumps(res, ensure_ascii=False),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    logger.info(f"Return: {ret}")
    return ret


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    payload = {}
    if event.get('body'):
        payload = event['body']
    return respond(None, payload)

if __name__ == '__main__':

    data = latent_diffusion("sunset over a lake in the mountains")
    print(data)
