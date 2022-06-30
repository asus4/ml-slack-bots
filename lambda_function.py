import argparse
import json
import logging
from urllib.parse import parse_qs
import requests

from app import slack, text2image

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def make_response(code: int, message: str):
    is_string = type(message) == str
    return {
        "statusCode": code,
        "headers": {
            "content-type": "text/plain" if is_string else "application/json",
        },
        "body": message if is_string else json.dumps(message, ensure_ascii=False),
    }


def normalize_header_case(header: dict):
    return {k.lower(): v for k, v in header.items()}


def post_slack(channel: str, user: str, message: str, attachments: list = None):
    text = f"<@{user}> {message}"

    if attachments is None:
        files = []
        for index, attachment in enumerate(attachments):
            res = slack.files_upload(filename=f"result-{index}.png", file=attachment)
            files.append(res["file"])
        files_markup = " ".join(f"<{file['permalink']}| >" for file in files)
        text += f"\nFiles: {files_markup}"

    return slack.chat_postMessage(channel=channel, text=text)


def slack_handler(event):
    print(f"Slack event: {json.dumps(event)}")

    content_type = event["headers"]["content-type"]

    body = (
        json.loads(event["body"])
        if content_type == "application/json"
        else parse_qs(event["body"])
    )

    if content_type == "application/json":
        type = body["type"]
        if type == "url_verification":
            # Just return the challenge for url_verification
            # https://api.slack.com/events/url_verification
            return make_response(200, body["challenge"])
        elif type == "event_callback":
            # Mention to @ml-playground
            slack_event = body["event"]
            channel = slack_event["channel"]
            user = slack_event["user"]
            usage = """Usage: 
            Type commands below to use the ML playground:

            ## Text to Image Models

            - Latent Diffusion Model:
            `/ml_latent_diffusion <your_prompt>`

            """
            slack.chat_postMessage(
                channel=channel,
                text=f"<@{user}> {usage}",
            )
            return make_response(200, {"status": "ok"})
        # else error
        return make_response(400, {"body": body})
    elif content_type == "application/x-www-form-urlencoded":
        # Event from slack command

        # Forward the event to internal_handler
        # As the slack api requires the response in 3000ms,
        request_content = event["requestContext"]
        url = "https://" + request_content["domainName"] + request_content["path"]
        try:
            res = requests.post(
                url=url,
                # https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-integration-async.html
                headers={
                    "InvocationType": "'Event'",
                    "Content-Type": "application/json",
                },
                json={
                    "channel": body["channel_id"],
                    "user": body["user_id"],
                    "command": body["command"],
                    "text": body["text"],
                },
                # timeout=0.5,  # Hack ignore response to return in 3sec
            )
            print(f"Response: {res}")
        except Exception as e:
            print(f"Error: {e}")
        return make_response(200, {"status": "ok"})
    # Unknown request
    print(f"Unknown request: {json.dumps(event)}")
    return make_response(400, {"error": "Unknown request"})


def internal_handler(event):
    print(f"Internal event: {json.dumps(event)}")

    # Get property from event
    body = json.loads(event["body"])
    command = body["command"]
    channel = body["channel"]
    user = body["user"]
    text = body["text"]

    message = ""
    attachments = None

    if command == "/ml_latent_diffusion":
        message = f"Your prompt: {text}"
        attachments = text2image.latent_diffusion(text, mock=False)
    else:
        return make_response(400, {"error": "Unknown command"})

    post_slack(
        channel=channel,
        user=user,
        message=message,
        attachments=attachments,
    )
    return make_response(200, {"status": "ok"})


def lambda_handler(event, context):
    """
    Entry point for the Lambda function.
    """
    print(f"Received event: {json.dumps(event)}")

    headers = normalize_header_case(event["headers"])
    event["headers"] = headers

    if "x-slack-signature" in headers:
        return slack_handler(event)
    else:
        return internal_handler(event)


if __name__ == "__main__":
    """
    Local test with
    python lambda_function.py --json test_event_data.json
    """
    parser = argparse.ArgumentParser(description="Test Lambda Function locally")
    parser.add_argument("--json", type=str, help="Test data in JSON format")
    args = parser.parse_args()

    with open(args.json) as f:
        event = json.load(f)
        result = lambda_handler(event, None)
        print(result)
