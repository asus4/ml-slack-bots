from argparse import _SubParsersAction
from email.policy import default
import replicate

from . import BaseCommand


class Erlich(BaseCommand):
    """
    Erlich Logo Generator
    https://replicate.com/laion-ai/erlich
    """

    def add_subparser(self, subparsers: _SubParsersAction):
        parser = subparsers.add_parser("erlich_logo", help="Erlich Logo Generator")
        parser.add_argument(
            "prompt", type=str, nargs="+", help="Prompt to generate images for"
        )
        parser.add_argument(
            "--guidance_scale",
            type=int,
            default=5,
            help="Classifier-free guidance scale. Higher values will result in more guidance toward caption, with diminishing returns. Try values between 1.0 and 40.0. In general, going above 5.0 will introduce some artifacting. (minimum: -20; maximum: 100)",
        )
        parser.add_argument(
            "--steps",
            type=int,
            default=100,
            help="Number of diffusion steps to run. Due to PLMS sampling, using more than 100 steps is unnecessary and may simply produce the exact same output. (minimum: 15; maximum: 250)",
        )
        parser.add_argument(
            "--batch_size",
            type=int,
            default=4,
            help="Batch size. (higher = slower) (minimum: 1; maximum: 16)",
        )
        parser.add_argument(
            "--width",
            type=int,
            default=256,
            help="Target width",
        )
        parser.add_argument(
            "--height",
            type=int,
            default=256,
            help="Target height",
        )
        parser.add_argument(
            "--aesthetic_rating",
            type=int,
            default=9,
            help="Aesthetic weight (0-1). How much to guide towards the aesthetic embed vs the prompt embed.",
        )

        parser.set_defaults(func=self.execute)
        return parser

    def execute(self, args):
        print(f"prompt: {args.prompt}")
        model = replicate.models.get("laion-ai/erlich")
        results = model.predict(
            prompt=self.merge_prompt(args.prompt),
            guidance_scale=args.guidance_scale,
            steps=args.steps,
            batch_size=args.batch_size,
            width=args.width,
            height=args.height,
            aesthetic_rating=args.aesthetic_rating,
        )

        print(f"erlich_logo results: {results}")
        urls = []
        for result in results:
            urls.extend(result)
        return urls
