import argparse
import json
from urllib.parse import parse_qsl
import requests


from app import slack, commands

active_commands: dict[str, commands.BaseCommand] = {
    "dalle_mini": commands.DalleMini(),
    "dalle_mega": commands.DalleMega(),
    "latent_diffusion": commands.LatentDiffusion(),
    "cogview2": commands.CogView2(),
    "erlich_logo": commands.Erlich(),
    "davinci": commands.Davinci(),
    "rinna_gpt2m": commands.RinnaGpt2Medium(),
}

_USAGE = """Usage: 
Type either of the following commands to try ML model:

- Try Dalle Mega: A mega version of Dalle.
`/ml_dalle_mega YOUR_PROMPT`

- Try Dalle Mini: A smaller version of Dalle.
`/ml_dalle_mini YOUR_PROMPT`

- Try Latent Diffusion:
`/ml_latent_diffusion YOUR_PROMPT`

- Try CogView2:
`/ml_cogview2 YOUR_PROMPT --style chinese`

CogView2 accepts style argument:
mainbody, photo, flat, comics, oil, sketch, isometric, chinese or watercolor

- Try Erlich Logo Generator:
`/ml_erlich_logo YOUR_PROMPT`

- Try Davinci:
`/ml_davinci YOUR_PROMPT`

- Try Rinna GPT2 Medium:
`/ml_rinna_gpt2m YOUR_PROMPT`

---

使い方. コマンドで好きなモデルを試せるよ

- Dalle-Mega を試したい時：
`/ml_dalle_mega 英語で文章`

- Dalle-Mini を試したい時：
`/ml_dalle_mini 英語で文章`

- Latent Diffusion Modelを試したい時:
`/ml_latent_diffusion 英語で文章`

- CogView2を試したい時:
`/ml_cogview2 英語で文章 --style chinese`

styleには以下のいずれかを指定することができます:
mainbody, photo, flat, comics, oil, sketch, isometric, chinese or watercolor

- Erlich Logo Generatorを試したい時:
`/ml_erlich_logo 英語で文章`

- Davinciを試したい時:
`/ml_davinci 英語で文章`

- Rinna GPT2 Mediumを試したい時:
`/ml_rinna_gpt2m 英語で文章`

"""


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


def post_slack(
    channel: str, user: str, message: str, attachments: list = None, links: list = None
):
    text = f"<@{user}> {message}"

    if attachments is not None:
        links = []
        for index, attachment in enumerate(attachments):
            res = slack.files_upload(filename=f"result-{index}.png", file=attachment)
            links.append(res["file"]["permalink"])

    if links is not None:
        links_markup = " ".join(f"<{link}| >" for link in links)
        text += f"\nLinks: {links_markup}"

    return slack.chat_postMessage(channel=channel, text=text)


def slack_handler(event):
    print(f"Slack event: {json.dumps(event)}")

    content_type = event["headers"]["content-type"]

    body = (
        json.loads(event["body"])
        if content_type == "application/json"
        else dict(parse_qsl(event["body"]))
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
            slack.chat_postMessage(
                channel=channel,
                text=f"<@{user}> {_USAGE}",
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
        command = body["command"]
        text = body["text"]
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
                    "command": command,
                    "text": text,
                },
                timeout=0.5,  # Hack ignore response to return in 3sec
            )
            print(f"Response: {res}")
        except Exception as e:
            print(f"Error: {e}")
        return make_response(200, f"Received your request: {command} {text}")
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

    message = f"`{command}`\nPrompt: {text}"

    parser = argparse.ArgumentParser(description="ML Playground")
    subparser = parser.add_subparsers(title="command")

    for key, cmd in active_commands.items():
        cmd.add_subparser(subparser)

    raw_args = text.split(" ")
    raw_args.insert(0, command.replace("/ml_", ""))
    args = parser.parse_args(raw_args)

    attachments = None
    links = None

    if command == "/ml_latent_diffusion":
        attachments = args.func(args)
    elif command == "/ml_dalle_mini":
        links = args.func(args)
    elif command == "/ml_dalle_mega":
        links = args.func(args)
    elif command == "/ml_cogview2":
        links = args.func(args)
        # Take first 4 items as many links are ignored in Slack
        # TODO: Upload them to slack then append to attachments?
        links = links[:4]
    elif command == "/ml_erlich_logo":
        links = args.func(args)
    elif command == "/ml_davinci":
        result = args.func(args)
        message = f"`{command}`\nPrompt: {text}\n\nResult:\n{result}"
    elif command == "/ml_rinna_gpt2m":
        result = args.func(args)
        message = f"`{command}`\nPrompt: {text}\n\nResult:\n{result}"
    else:
        return make_response(
            400,
            {
                "error": "Unknown command",
                "text": text,
            },
        )

    post_slack(
        channel=channel,
        user=user,
        message=message,
        attachments=attachments,
        links=links,
    )
    return make_response(200, {"status": "ok"})


def lambda_handler(event, context):
    """
    Entry point for the Lambda function.
    """
    print(f"Received event: {json.dumps(event)}")

    headers = normalize_header_case(event["headers"])
    event["headers"] = headers

    if "X-Slack-Retry-Num" in headers:
        # Slack API retries if it doesn't get a response in 3000ms
        # Ignore retry event
        print("Ignoring retry event")
        return make_response(200, {"status": "ok"})

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
