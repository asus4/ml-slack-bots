import argparse
import base64
import json
import requests

from . import BaseCommand
from .. import Config


def find_images(obj):
    images = []

    if type(obj) is dict:
        for _, value in obj.items():
            images.extend(find_images(value))
    elif type(obj) is list:
        for item in obj:
            images.extend(find_images(item))
    elif type(obj) is str:
        # Decode base64 to png binary
        if obj.startswith("data:image/png;base64,"):
            txt = obj.replace("data:image/png;base64,", "")
            images.append(base64.b64decode(txt, validate=True))
    return images


class LatentDiffusion(BaseCommand):
    """
    latent diffusion model
    https://hf.space/embed/multimodalart/latentdiffusion/api
    """

    def add_subparser(self, subparsers: argparse._SubParsersAction):
        parser = subparsers.add_parser("latent_diffusion", help="Latent Diffusion")
        parser.add_argument(
            "prompt", type=str, nargs="+", help="Prompt to generate images for"
        )
        parser.add_argument("--steps", type=int, default=50, help="Number of steps")
        parser.add_argument(
            "--width",
            type=int,
            default=256,
            help="Width of the image",
            choices=[32, 64, 128, 256],
        )
        parser.add_argument(
            "--height",
            type=int,
            default=256,
            help="Height of the image",
            choices=[32, 64, 128, 256],
        )
        parser.add_argument(
            "--images",
            type=int,
            default=4,
            help="Number of images to generate",
            choices=[1, 2, 3, 4],
        )
        parser.add_argument(
            "--diversity_scale",
            type=int,
            default=5,
            help="Diversity scale",
        )

        parser.set_defaults(func=self.execute)
        return parser

    def execute(self, args):
        return self.latent_diffusion(
            prompt=self.merge_prompt(args.prompt),
            steps=args.steps,
            width=args.width,
            height=args.height,
            images=args.images,
            diversity_scale=args.diversity_scale,
        )

    def latent_diffusion(
        self,
        prompt: str,
        steps=50,
        width=256,
        height=256,
        images=4,
        diversity_scale=5,
        mock=False,
    ):

        response = None

        if mock:
            response = self.mock_response("test/latent_diffusion.json")
        else:
            res = requests.post(
                url="https://hf.space/embed/multimodalart/latentdiffusion/+/api/predict/",
                headers={"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"},
                json={
                    "data": [
                        prompt,
                        steps,
                        str(width),
                        str(height),
                        images,
                        diversity_scale,
                    ]
                },
            )
            response = res.json()
            print(f"latent_diffusion json: {json.dumps(response)}")

            # for debug
            # save_response(res, "test/latent_diffusion.json")

        return find_images(response["data"][1])
