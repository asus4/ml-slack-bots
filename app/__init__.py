
from .config import Config
from slack_sdk import WebClient

slack = WebClient(token=Config.SLACK_BOT_OAUTH_TOKEN)
