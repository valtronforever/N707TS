import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error
import json


#def run(addr, op_id, psswd):
#    url = 'http://' + addr + '/cgi/tbl/whiteIP'
#    #r = requests.get(url, auth=HTTPDigestAuth(op_id, psswd))
#    payload = [{
#        'id': 1,
#        'IP': '0.0.0.0',
#        'Login': '',
#    }]
#    headers = {'X-HTTP-Method-Override': 'PATCH'}
#    r = requests.post(
#        url,
#        data=json.dumps(payload, ensure_ascii=False),
#        auth=HTTPDigestAuth(op_id, psswd),
#        headers=headers
#    )
#    if not check_error(r):
#        print('OK')
#        print(r.json())


def run(addr, op_id, psswd, timeout, print_timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/proc/register'
    if getattr(cmd_args, 'clear', False):
        r = requests.get(url, params='clear', auth=HTTPDigestAuth(op_id, psswd), timeout=timeout)
    else:
        r = requests.get(url, auth=HTTPDigestAuth(op_id, psswd), timeout=timeout)
    if not check_error(r, json_out=cmd_args.json):
        if cmd_args.json:
            print(json.dumps({'result': 'ok'}))
        else:
            print('OK')
