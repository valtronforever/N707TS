import requests
import json
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/chk'
    params = {}
    start_id = getattr(cmd_args, 'id', None)
    if start_id:
        params['id'] = start_id
    r = requests.get(url, params=params, auth=HTTPDigestAuth(op_id, psswd), timeout=timeout)
    if not check_error(r, json_out=cmd_args.json):
        if cmd_args.out:
            json.dump(r.json(), cmd_args.out)
            if cmd_args.json:
                print(json.dumps({
                    'result': 'ok',
                }))
            else:
                print('Ok')
        else:
            print(json.dumps(r.json()))
