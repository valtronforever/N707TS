import requests
import json
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, print_timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/proc/getjrnroom'
    r = requests.get(url, auth=HTTPDigestAuth(op_id, psswd), timeout=timeout)
    if not check_error(r, json_out=cmd_args.json):
        data = r.json()
        if cmd_args.json:
            print(json.dumps({
                'result': 'ok',
                'response': r.json(),
            }))
        else:
            print("%s%s" % (
                ('Total:').ljust(10),
                data['Total'],
            ))
            print("%s%s" % (
                ('Used:').ljust(10),
                data['Used'],
            ))
