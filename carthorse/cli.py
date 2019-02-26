import os
from argparse import ArgumentParser

from .config import load_config
from . import version_from, when, actions


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--config', default='pyproject.toml')
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config)

    config.version = config.run(version_from, config['version-from'])
    os.environ['VERSION'] = config.version

    ok = True
    for check in config['when']:
        ok = config.run(when, check)
        if not ok:
            break

    if ok:
        for action in config['actions']:
            config.run(actions, action)
