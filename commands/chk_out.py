# coding: utf8

import json
import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, print_timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/chk'
    io = {'sum': cmd_args.amount*-1}
    if cmd_args.no:
        io['no'] = cmd_args.no
    payload = {'IO': [{'IO': io}]}
    r = requests.post(
        url,
        data=json.dumps(payload, ensure_ascii=False),
        auth=HTTPDigestAuth(op_id, psswd),
        timeout=print_timeout,
    )
    if not check_error(r, json_out=cmd_args.json):
        if cmd_args.json:
            print(json.dumps({'result': 'ok'}))
        else:
            print('OK')
