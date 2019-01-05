import json
import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, print_timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/scr'
    r = requests.get(
        url,
        auth=HTTPDigestAuth(op_id, psswd),
        timeout=timeout,
    )
    if not check_error(r, json_out=cmd_args.json):
        if cmd_args.json:
            print(json.dumps({
                'result': 'ok',
                'response': r.json(),
            }))
        else:
            info = r.json()
            print('Width:  %d' % info['chars']['w'])
            print('Height: %d' % info['chars']['h'])
