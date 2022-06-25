import argparse
import json
import logging
import requests

from app import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def make_response(err, res=None):
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
    res = requests.post(
        url="https://slack.com/api/chat.postMessage",
        headers={
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Bearer {Config.SLACK_BOT_OAUTH_TOKEN}",
        },
        json={
            "token": Config.SLACK_VERIFICATION_TOKEN,
            "channel": channel,
            "text": message,
        },
    )
    logger.info(f"status: {res.status_code} content: {res.content}")
    return res.status_code == 200


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    body = json.loads(event["body"])
    print(body)
    type = body["type"]

    if type == "url_verification":
        # Just return the challenge for url_verification
        # https://api.slack.com/events/url_verification
        return {
            "statusCode": "200",
            "body": body["challenge"],
            "headers": {"Content-Type": "text/plain"},
        }
    elif type == "event_callback":
        channel = body["event"]["channel"]
        text_args = body["event"]["text"].split(" ")
        message = " ".join(text_args[1:])
        post_slack(channel, message)
    return make_response(None, body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Lambda Function locally")
    parser.add_argument("--json", type=str, help="Test data in JSON format")
    args = parser.parse_args()

    with open(args.json) as f:
        event = json.load(f)
        result = lambda_handler(event, None)
        print(result)
