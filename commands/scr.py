import json
import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/scr'
    payload = [{
        'id': cmd_args.line,
        'str': cmd_args.text,
        'align': cmd_args.align,
    }]
    r = requests.post(
        url,
        data=json.dumps(payload, ensure_ascii=False),
        auth=HTTPDigestAuth(op_id, psswd),
        timeout=timeout,
    )
    if not check_error(r, json_out=cmd_args.json):
        if cmd_args.json:
            print(json.dumps({'result': 'ok'}))
        else:
            print('OK')
