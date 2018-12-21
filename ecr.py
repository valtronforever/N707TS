# coding: utf8

import argparse
import textwrap
from configparser import ConfigParser
from commands import dev_info, state, scr, oper, rep_pay, printreport, getjrnroom, chk, register, whiteip


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

    parser_state = subparsers.add_parser('state', help='Get and print device state')
    parser_state.set_defaults(func=lambda _: state.run(*list_config()))

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

    parser_whiteip = subparsers.add_parser('whiteip', help='Print white ip table')
    parser_whiteip.set_defaults(func=lambda cmd_args: whiteip.run(*list_config(), cmd_args=cmd_args))

    parser_register = subparsers.add_parser('register', help='Register operator ip')
    parser_register.add_argument('-c', '--clear', action='store_true', help='Remove current operator from whitelist')
    parser_register.set_defaults(func=lambda _: register.run(*list_config()))

    parser_rep_pay = subparsers.add_parser('rep_pay', help='Get cash amount in cashbox')
    parser_rep_pay.set_defaults(func=lambda _: rep_pay.run(*list_config()))

    parser_getjrnroom = subparsers.add_parser('getjrnroom', help='Get journal total and used space')
    parser_getjrnroom.set_defaults(func=lambda _: getjrnroom.run(*list_config()))

    parser_printreport = subparsers.add_parser('printreport', help='Print report')
    parser_printreport.add_argument('rep_no', choices=['0', '1', '10', '20', '21'], help=textwrap.dedent(u'''\
    Report No:
    0 - Дневной обнуляющий отчет,
    1 - Отчет по обнулению электронной ленты,
    10 - Дневной отчет без обнуления,
    20 - Отчет по проданным товарам,
    21 - Отчет по проданным товарам с обнулением этого отчета
    '''))
    parser_printreport.set_defaults(func=lambda cmd_args: printreport.run(*list_config(), cmd_args=cmd_args))

    parser_chk = subparsers.add_parser('chk', help='Print receipt')
    parser_chk.add_argument('json_file', type=argparse.FileType('r'), help='Receipt file in json format')
    parser_chk.set_defaults(func=lambda cmd_args: chk.run(*list_config(), cmd_args=cmd_args))

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
