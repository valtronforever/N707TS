import requests
from requests.auth import HTTPDigestAuth


def run(addr, op_id, psswd):
    url = 'http://' + addr + '/cgi/dev_info'
    r = requests.get(url, auth=HTTPDigestAuth(op_id, psswd))
    if r.status_code != 200:
        raise Exception

    for k, v in r.json().items():
        print("%s%s" % (
            (k + ':').ljust(10),
            v,
        ))
