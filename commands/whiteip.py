import requests
from requests.auth import HTTPDigestAuth
from configparser import ConfigParser
from utils.errors import check_error


def run(addr, op_id, psswd, cmd_args=None):
    url = 'http://' + addr + '/cgi/tbl/whiteIP'

    # Request only as service
    r = requests.get(url, auth=HTTPDigestAuth('service', '751426'))
    if not check_error(r):
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
