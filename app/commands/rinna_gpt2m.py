import argparse
import json
import requests
from huggingface_hub.inference_api import InferenceApi

from . import BaseCommand
from .. import Config


class RinnaGpt2Medium(BaseCommand):
    """
    Rinna Japanese GPT2 model
    https://huggingface.co/rinna/japanese-gpt2-medium
    """

    def add_subparser(self, subparsers: argparse._SubParsersAction):
        parser = subparsers.add_parser("rinna_gpt2m", help="Rinna Japanese GPT2 Medium")
        parser.add_argument(
            "prompt", type=str, nargs="+", help="Prompt to generate images for"
        )
        parser.set_defaults(func=self.execute)
        return parser

    def execute(self, args):
        prompt = self.merge_prompt(args.prompt)
        print(f"Rinna prompt: {prompt}")

        inference = InferenceApi(
            repo_id="rinna/japanese-gpt2-medium",
            token=Config.HUGGINGFACE_API_TOKEN,
            gpu=True,
        )
        response = inference(inputs=prompt)
        print(f"Rinna json: {json.dumps(response)}")
        return response[0]["generated_text"]
