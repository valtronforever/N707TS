# coding: utf8

import json
import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, cmd_args=None):
    url = 'http://' + addr + '/cgi/chk'
    r = requests.post(
        url,
        data=cmd_args.json_file.read(),
        auth=HTTPDigestAuth(op_id, psswd),
    )
    if not check_error(r):
        print('OK')
