import argparse
import json
import logging

from app import slack, text2image

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def make_response(code: int, message: str):
    is_string = type(message) == str
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "text/plain" if is_string else "application/json",
        },
        "body": message if is_string else json.dumps(message, ensure_ascii=False),
    }


def parse_slack_event(event):
    """
    Parse a Slack mention and return the user ID.
    """
    channel = event["channel"]
    user = event["user"]
    text_args = event["text"].split(" ")
    prompt = " ".join(text_args[1:])

    return channel, user, prompt


def lambda_handler(event, context):
    """
    Entry point for the Lambda function.
    """
    logger.info(f"Received event:\n {json.dumps(event)}")

    body = json.loads(event["body"])
    print(body)
    type = body["type"]

    if type == "url_verification":
        # Just return the challenge for url_verification
        # https://api.slack.com/events/url_verification
        return make_response(200, body["challenge"])
    elif type == "event_callback":
        channel, user, prompt = parse_slack_event(body["event"])

        images = text2image.latent_diffusion(prompt, mock=False)

        files = []
        for index, image in enumerate(images):
            res = slack.files_upload(filename=f"result-{index}.png", file=image)
            files.append(res["file"])

        files_markup = " ".join(f"<{file['permalink']}| >" for file in files)
        slack.chat_postMessage(
            channel=channel,
            text=f"<@{user}> Your prompt: {prompt}\nResult: {files_markup}",
        )
        return make_response(200, {"body": body})
    else:
        return make_response(400, {"body": body})


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
