import argparse
import replicate

from . import BaseCommand


class StableDiffusion(BaseCommand):
    """
    Stable Diffusion model
    https://replicate.com/stability-ai/stable-diffusion
    """

    def add_subparser(self, subparsers: argparse._SubParsersAction):
        parser = subparsers.add_parser("stable_diffusion", help="Stable Diffusion")
        parser.add_argument(
            "prompt", type=str, nargs="+", help="Prompt to generate images for"
        )
        parser.add_argument(
            "--num_outputs",
            type=int,
            default=1,
            help="Number of images to output",
            choices=[1, 4],
        )
        parser.add_argument(
            "--num_inference_steps",
            type=int,
            default=100,
            help="Number of denoising steps (minimum: 1; maximum: 500)",
        )
        parser.add_argument(
            "--guidance_scale",
            type=float,
            default=7.5,
            help="Scale for classifier-free guidance (minimum: 1; maximum: 20)",
        )
        parser.add_argument(
            "--width",
            type=int,
            default=256,
            help="Width of output image",
            choices=[128, 256, 512, 768, 1024],
        )
        parser.add_argument(
            "--height",
            type=int,
            default=256,
            help="Height of output image",
            choices=[128, 256, 512, 768],
        )
        parser.set_defaults(func=self.execute)
        return parser

    def execute(self, args):
        print(f"prompt: {args.prompt}")
        model = replicate.models.get("stability-ai/stable-diffusion")
        results = model.predict(
            prompt=self.merge_prompt(args.prompt),
            num_outputs=args.num_outputs,
            num_inference_steps=args.num_inference_steps,
            guidance_scale=args.guidance_scale,
            width=args.width,
            height=args.height,
        )

        resultsList = list(results)
        print(f"stable-diffusion results: {resultsList}")
        return resultsList
