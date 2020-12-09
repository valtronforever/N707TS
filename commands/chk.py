# coding: utf8

import json
import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, print_timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/chk'
    r = requests.post(
        url,
        data=cmd_args.json_file.read().encode('utf-8'),
        auth=HTTPDigestAuth(op_id, psswd),
        timeout=print_timeout,
    )
    if not check_error(r, json_out=cmd_args.json):
        if cmd_args.json:
            print(json.dumps({
                'result': 'ok',
                'response': r.json(),
            }))
        else:
            print('OK')
