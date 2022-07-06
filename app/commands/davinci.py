import argparse
import json
import requests

from . import BaseCommand
from .. import Config


class Davinci(BaseCommand):
    """
    OpenAI Davinci GPT-3 model
    https://beta.openai.com/examples/
    """

    def add_subparser(self, subparsers: argparse._SubParsersAction):
        parser = subparsers.add_parser("davinci", help="OpenAI Davinci GPT")
        parser.add_argument(
            "prompt", type=str, nargs="+", help="Prompt to generate images for"
        )
        parser.add_argument(
            "--temperature",
            type=float,
            default=0.7,
            help="Controls randomness: Lowering results in less random completions.",
        )
        parser.add_argument(
            "--max_tokens",
            type=int,
            default=128,
            help="Maximum number of tokens to generate",
        )
        parser.add_argument(
            "--top_p",
            type=float,
            default=1.0,
            help="Controls diversity via nucleus sampling",
        )
        parser.add_argument(
            "--frequency_penalty",
            type=float,
            default=0.0,
            help="How much to penalize new tokens based on their existing frequency in the text so far.",
        )
        parser.add_argument(
            "--presence_penalty",
            type=float,
            default=0.0,
            help="How much to penalize new tokens based on whether they appear in the text so far.",
        )
        parser.set_defaults(func=self.execute)
        return parser

    def execute(self, args):
        prompt = self.merge_prompt(args.prompt) + "\n\n"
        print(f"Davinci prompt: {prompt}")

        res = requests.post(
            url="https://api.openai.com/v1/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
            },
            data=json.dumps(
                {
                    "model": "text-davinci-002",
                    "prompt": prompt,
                    "temperature": args.temperature,
                    "max_tokens": args.max_tokens,
                    "top_p": args.top_p,
                    "frequency_penalty": args.frequency_penalty,
                    "presence_penalty": args.presence_penalty,
                }
            ),
        )
        response = res.json()
        print(f"Davinci json: {json.dumps(response)}")
        return response["choices"][0]["text"]
