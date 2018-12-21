import json
import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, cmd_args=None):
    url = 'http://' + addr + '/cgi/proc/printreport'
    r = requests.get(url, params=cmd_args.rep_no, auth=HTTPDigestAuth(op_id, psswd))
    if not check_error(r):
        print('OK')
