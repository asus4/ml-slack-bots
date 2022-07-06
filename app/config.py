import os


class Config:
    # Load Tokens from .env file
    HUGGINGFACE_API_TOKEN = os.environ["HUGGINGFACE_API_TOKEN"]
    REPLICATE_API_TOKEN = os.environ["REPLICATE_API_TOKEN"]
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    SLACK_BOT_OAUTH_TOKEN = os.environ["SLACK_BOT_OAUTH_TOKEN"]
    SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
