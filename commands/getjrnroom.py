import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd):
    url = 'http://' + addr + '/cgi/proc/getjrnroom'
    r = requests.get(url, auth=HTTPDigestAuth(op_id, psswd))
    if not check_error(r):
        data = r.json()
        print("%s%s" % (
            ('Total:').ljust(10),
            data['Total'],
        ))
        print("%s%s" % (
            ('Used:').ljust(10),
            data['Used'],
        ))
