import argparse
import json
import logging
import requests

from app import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def respond(err, res=None):
    ret = {
        "statusCode": "200",
        "body": json.dumps(res, ensure_ascii=False),
        "headers": {
            "Content-Type": "application/json",
        },
    }
    logger.info(f"Return: {ret}")
    return ret


def post_slack(channel, message):
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {Config.SLACK_BOT_OAUTH_TOKEN}",
    }
    url = "https://slack.com/api/chat.postMessage"
    payload = {
        "text": message,
        "token": Config.SLACK_VERIFICATION_TOKEN,
        "channel": channel,
    }
    logger.info(f"Header: {headers} Payload: {payload}")
    res = requests.post(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    logger.info(f"status: {res.status_code} content: {res.content}")


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    body = json.loads(event["body"])
    print(body)

    # https://api.slack.com/events/url_verification
    # Just return the challenge for url_verification
    type = body["type"]
    if type == "url_verification":
        return {
            "statusCode": "200",
            "body": body["challenge"],
            "headers": {"Content-Type": "text/plain"},
        }
    elif type == "event_callback":
        channel = body["event"]["channel"]
        text_args = body['event']['text'].split(' ')
        message = ' '.join(text_args[1:])
        post_slack(channel, message)
    return respond(None, body)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Lambda Function locally")
    parser.add_argument("--json", type=str, help="Test data in JSON format")
    args = parser.parse_args()

    with open(args.json) as f:
        event = json.load(f)
        result = lambda_handler(event, None)
        print(result)
