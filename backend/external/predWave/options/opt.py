import argparse
import multiprocessing


class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--name", required=True, type=str, default="default", help=""
        )
        self.parser.add_argument(
            "--data_list",
            required=True,
            type=str,
            default="default",
            help="Path for data list",
        )

    def parse(self):
        self.opt = self.parser.parse_args()
        return self.opt
