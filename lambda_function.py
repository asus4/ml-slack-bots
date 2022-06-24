import argparse
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
    
    body = json.loads(event['body'])
    print(body)

    # https://api.slack.com/events/url_verification
    # Just return the challenge for url_verification
    type = body['type']
    if type == 'url_verification':
        return {
            'statusCode': '200',
            'body': body['challenge'],
            'headers': { 'Content-Type': 'text/plain' },
        }
    return respond(None, body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Lambda Function locally')
    parser.add_argument('--json', type=str, help='Test data in JSON format')
    args = parser.parse_args()

    with open(args.json) as f:
        event = json.load(f)
        result = lambda_handler(event, None)
        print(result)
