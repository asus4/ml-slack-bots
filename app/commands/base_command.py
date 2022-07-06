from abc import ABC, abstractmethod
import argparse
import json


class BaseCommand(ABC):
    @abstractmethod
    def add_subparser(self, subparsers: argparse._SubParsersAction):
        pass

    @abstractmethod
    def execute(self, args):
        pass

    def save_response(self, response, filename: str):
        with open(filename, "wb") as f:
            f.write(response.content)

    def mock_response(self, filename: str):
        with open(filename, "r") as f:
            return json.load(f)

    def merge_prompt(self, prompt: list[str]):
        return " ".join(prompt)
