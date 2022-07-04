from argparse import _SubParsersAction
import replicate

from . import BaseCommand


class DalleMini(BaseCommand):
    """
    Dalle Mini model
    https://replicate.com/borisdayma/dalle-mini
    """

    def add_subparser(self, subparsers: _SubParsersAction):
        parser = subparsers.add_parser("dalle_mini", help="Dalle Mini")
        parser.add_argument(
            "prompt", type=str, nargs="+", help="Prompt to generate images for"
        )
        parser.add_argument(
            "--n_predictions", type=int, default=4, help="Number of images to generate"
        )

        parser.set_defaults(func=self.execute)
        return parser

    def execute(self, args):
        print(f"prompt: {args.prompt}")
        model = replicate.models.get("borisdayma/dalle-mini")
        results = model.predict(
            prompt=self.merge_prompt(args.prompt),
            n_predictions=args.n_predictions,
        )

        print(f"dalle_mini results: {results}")
        return list((result["image"] for result in results))
