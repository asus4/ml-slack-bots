import argparse
import replicate

from . import BaseCommand


class DalleMega(BaseCommand):
    """
    Dalle Mega model
    https://replicate.com/kuprel/min-dalle
    """

    def add_subparser(self, subparsers: argparse._SubParsersAction):
        parser = subparsers.add_parser("dalle_mega", help="Dalle Mega")
        parser.add_argument(
            "prompt", type=str, nargs="+", help="Prompt to generate images for"
        )
        parser.add_argument(
            "--grid_size",
            type=int,
            default=3,
            help="Size of the image grid (minimum: 1; maximum: 4)",
        )
        parser.add_argument(
            "--intermediate_outputs",
            default=False,
            action=argparse.BooleanOptionalAction,
        )
        parser.add_argument(
            "--supercondition_factor",
            type=int,
            default=16,
            help="Higher values result in better agreement with the text but a narrower variety of generated images (minimum: 1; maximum: 6)",
        )

        parser.set_defaults(func=self.execute)
        return parser

    def execute(self, args):
        print(f"prompt: {args.prompt}")
        model = replicate.models.get("kuprel/min-dalle")
        results = model.predict(
            text=self.merge_prompt(args.prompt),
            grid_size=args.grid_size,
            intermediate_outputs=args.intermediate_outputs,
            supercondition_factor=args.supercondition_factor,
        )

        resultsList = list(results)
        print(f"dalle_mega results: {resultsList}")
        return [resultsList.pop()]
