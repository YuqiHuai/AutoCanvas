from argparse import ArgumentParser
from configparser import ConfigParser

from api import API
from scripts import Script
from scripts.DiscussionParticipation import DiscussionParticipation
from utils.config import Config


class ScriptRunner:
    def __init__(self, script: Script):
        self.__script = script

    def run(self):
        self.__script.run()


def main(config_file):
    # initialize
    config_parser = ConfigParser()
    config_parser.read(config_file)
    config = Config(config_parser)
    API(config)  # initialize API to register AUTH_TOKEN

    # initialize script and runner
    script = DiscussionParticipation()
    runner = ScriptRunner(script)
    runner.run()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file)
