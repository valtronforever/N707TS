import argparse
from configparser import ConfigParser
from commands import dev_info


def get_config():
    config = ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']


def list_config():
    c = get_config()
    return c['addr'], c['op_id'], c['op_psswd']


def run_dev_info(*args):
    dev_info.run(*list_config())


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='subcommands',
    )

    parser_dev_info = subparsers.add_parser('dev_info', help='Get and print device info')
    parser_dev_info.set_defaults(func=run_dev_info)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
