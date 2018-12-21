import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd):
    url = 'http://' + addr + '/cgi/dev_info'
    r = requests.get(url, auth=HTTPDigestAuth(op_id, psswd))
    if not check_error(r):
        for k, v in r.json().items():
            print("%s%s" % (
                (k + ':').ljust(10),
                v,
            ))
