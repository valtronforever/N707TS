import requests
import json
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/tbl/whiteIP'

    # Request only as service
    r = requests.get(url, auth=HTTPDigestAuth('service', '751426'), timeout=timeout)
    if not check_error(r, json_out=cmd_args.json):
        if cmd_args.json:
            print(json.dumps({
                'result': 'ok',
                'response': r.json(),
            }))
        else:
            print("%s | %s | %s |" % (
                'Id'.ljust(3),
                'Ip'.ljust(32),
                'Login'.ljust(10),
            ))
            print('-'*53)
            for ip in r.json():
                print("%s | %s | %s" % (
                    str(ip['id']).rjust(3),
                    ip['IP'].ljust(32),
                    ip['Login'].ljust(32),
                ))
