# coding: utf8

import argparse
import os
import sys
import textwrap
import requests
import json
from configparser import ConfigParser
from commands import devices, dev_info, state, scr_info, scr, scr_multi, oper, rep_pay, printreport, getjrnroom, chk, chk_copy, chk_empty,\
    chk_sync, register, whiteip, chk_in, chk_out


def get_config(path):
    config = ConfigParser()
    config.read(path)
    return config['DEFAULT']


def list_config(path):
    c = get_config(path)
    return c['addr'], c['op_id'], c['op_psswd'], float(c['timeout']), float(c['print_timeout'])


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # return an open file handle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='config.ini', type=lambda x: is_valid_file(parser, x),
                        help='Specify custom path to config file')
    parser.add_argument('--json', action='store_true', help='Output info in json format')
    subparsers = parser.add_subparsers(
        title='subcommands', metavar='{command} -h'
    )

    parser_devices = subparsers.add_parser('devices', help='Get all devices available in current network')
    parser_devices.set_defaults(func=lambda cmd_args: devices.run(cmd_args=cmd_args))

    parser_dev_info = subparsers.add_parser('dev_info', help='Get and print device info')
    parser_dev_info.set_defaults(func=lambda cmd_args: dev_info.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_state = subparsers.add_parser('state', help='Get and print device state')
    parser_state.set_defaults(func=lambda cmd_args: state.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_scr_info = subparsers.add_parser('scr_info', help='Get info about ecr screen')
    parser_scr_info.set_defaults(func=lambda cmd_args: scr_info.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_scr = subparsers.add_parser('scr', help='Print info on client screen')
    parser_scr.add_argument('-l', '--line', choices=['1', '2', '3', '4'], required=True,
                            help='The line on which information will be displayed')
    parser_scr.add_argument('-a', '--align', choices=['l', 'r', 'c'], default='c',
                            help='Text align')
    parser_scr.add_argument('text', help='Message text')
    parser_scr.set_defaults(func=lambda cmd_args: scr.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_scr_multi = subparsers.add_parser('scr_multi', help='Print info on client screen (multiple lines form json file)')
    parser_scr_multi.add_argument('json_str', help='Lines in json format according to dev doc')
    parser_scr_multi.set_defaults(func=lambda cmd_args: scr_multi.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_oper = subparsers.add_parser('oper', help='Print all available operators')
    parser_oper.add_argument('-s', '--set', choices=range(1, 33), type=int, metavar='id',
                            help='Set operator as active and store appropriate id and password to config')
    parser_oper.add_argument('--service', action='store_true', help='Set service as active operator')
    parser_oper.set_defaults(func=lambda cmd_args: oper.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_whiteip = subparsers.add_parser('whiteip', help='Print white ip table')
    parser_whiteip.set_defaults(func=lambda cmd_args: whiteip.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_register = subparsers.add_parser('register', help='Register operator ip')
    parser_register.add_argument('-c', '--clear', action='store_true', help='Remove current operator from whitelist')
    parser_register.set_defaults(func=lambda cmd_args: register.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_rep_pay = subparsers.add_parser('rep_pay', help='Get cash amount in cashbox')
    parser_rep_pay.set_defaults(func=lambda cmd_args: rep_pay.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_getjrnroom = subparsers.add_parser('getjrnroom', help='Get journal total and used space')
    parser_getjrnroom.set_defaults(
        func=lambda cmd_args: getjrnroom.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_printreport = subparsers.add_parser('printreport', help='Print report')
    parser_printreport.add_argument('rep_no', choices=['0', '1', '10', '20', '21'], help=textwrap.dedent(u'''\
    Report No:
    0 - Дневной обнуляющий отчет,
    1 - Отчет по обнулению электронной ленты,
    10 - Дневной отчет без обнуления,
    20 - Отчет по проданным товарам,
    21 - Отчет по проданным товарам с обнулением этого отчета
    '''))
    parser_printreport.set_defaults(
        func=lambda cmd_args: printreport.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_chk = subparsers.add_parser('chk', help='Print receipt')
    parser_chk.add_argument('json_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                            help='Receipt file in json format (empty - read stdin)')
    parser_chk.set_defaults(func=lambda cmd_args: chk.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_chk_in = subparsers.add_parser('chk_in', help='Print money deposit receipt')
    parser_chk_in.add_argument('-n', '--no', type=int, default=1, help='Payment No (default: 1)')
    parser_chk_in.add_argument('amount', type=float, help='Money amount for deposit')
    parser_chk_in.set_defaults(func=lambda cmd_args: chk_in.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_chk_out = subparsers.add_parser('chk_out', help='Print money withdrawal receipt')
    parser_chk_out.add_argument('-n', '--no', type=int, default=1, help='Payment No (default: 1)')
    parser_chk_out.add_argument('amount', type=float, help='Money amount for withdrawal')
    parser_chk_out.set_defaults(func=lambda cmd_args: chk_out.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_chk_copy = subparsers.add_parser('chk_copy', help='Print copy of last receipt')
    parser_chk_copy.set_defaults(func=lambda cmd_args: chk_copy.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_chk_empty = subparsers.add_parser('chk_empty', help='Print empty receipt (open session)')
    parser_chk_empty.set_defaults(func=lambda cmd_args: chk_empty.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    parser_chk_sync = subparsers.add_parser('chk_sync', help='Get receipt journal')
    parser_chk_sync.add_argument('-o', '--out', type=argparse.FileType('w'), help='Output filename (default: stdout)')
    parser_chk_sync.add_argument('--id', help='Start from specified id')
    parser_chk_sync.set_defaults(func=lambda cmd_args: chk_sync.run(*list_config(cmd_args.config), cmd_args=cmd_args))

    args = parser.parse_args()
    try:
        args.func(args)
    except requests.exceptions.Timeout:
        if args.json:
            print(json.dumps({
                'result': 'error',
                'message': 'Connection timeout',
            }))
        else:
            print("Error, connection timeout")
    except requests.exceptions.ConnectionError:
        if args.json:
            print(json.dumps({
                'result': 'error',
                'message': 'Connection refused',
            }))
        else:
            print("Error, connection refused")


if __name__ == "__main__":
    main()
