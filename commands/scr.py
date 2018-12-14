import json
import requests
from requests.auth import HTTPDigestAuth


def run(addr, op_id, psswd, cmd_args=None):
    url = 'http://' + addr + '/cgi/scr'
    payload = [{
        'id': cmd_args.line,
        'str': cmd_args.text,
        'align': cmd_args.align,
    }]
    r = requests.post(url, data=json.dumps(payload, ensure_ascii=False), auth=HTTPDigestAuth(op_id, psswd))
    if r.status_code != 200:
        raise Exception
    print('OK')
