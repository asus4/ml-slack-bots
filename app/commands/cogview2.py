from argparse import _SubParsersAction
import replicate

from . import BaseCommand


class CogView2(BaseCommand):
    """
    Cog View2 model
    https://replicate.com/thudm/cogview2
    """

    def add_subparser(self, subparsers: _SubParsersAction):
        parser = subparsers.add_parser("cogview2", help="CogView2")
        parser.add_argument(
            "prompt",
            metavar="prompt",
            type=str,
            nargs="+",
            help="Prompt to generate images for",
        )
        parser.add_argument(
            "--style",
            default="mainbody",
            help="Style",
            choices=[
                "none",
                "mainbody",
                "photo",
                "flat",
                "comics",
                "oil",
                "sketch",
                "isometric",
                "chinese",
                "watercolor",
            ],
        )

        parser.set_defaults(func=self.execute)
        return parser

    def execute(self, args):
        print(f"prompt: {args.prompt}")
        model = replicate.models.get("thudm/cogview2")
        results = model.predict(
            prompt=args.prompt,
            style=args.style,
        )

        print(f"cogview2 results: {results}")
        return list((result["image"] for result in results))
