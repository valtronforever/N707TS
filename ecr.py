import argparse
from configparser import ConfigParser
from commands import dev_info, scr, oper


def get_config():
    config = ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']


def list_config():
    c = get_config()
    return c['addr'], c['op_id'], c['op_psswd']


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='subcommands', metavar='{command} -h'
    )

    parser_dev_info = subparsers.add_parser('dev_info', help='Get and print device info')
    parser_dev_info.set_defaults(func=lambda _: dev_info.run(*list_config()))

    parser_scr = subparsers.add_parser('scr', help='Print info on client screen')
    parser_scr.add_argument('-l', '--line', choices=['1', '2', '3', '4'], required=True,
                            help='The line on which information will be displayed')
    parser_scr.add_argument('-a', '--align', choices=['l', 'r', 'c'], default='c',
                            help='Text align')
    parser_scr.add_argument('text', help='Message text')
    parser_scr.set_defaults(func=lambda cmd_args: scr.run(*list_config(), cmd_args=cmd_args))

    parser_oper = subparsers.add_parser('oper', help='Print all available operators')
    parser_oper.add_argument('-s', '--set', choices=range(1, 33), type=int, metavar='id',
                            help='Set operator as active and store appropriate id and password to config')
    parser_oper.add_argument('--service', action='store_true', help='Set service as active operator')
    parser_oper.set_defaults(func=lambda cmd_args: oper.run(*list_config(), cmd_args=cmd_args))

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
