import requests
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd):
    pay_info_url = 'http://' + addr + '/cgi/tbl/Pay'
    pay_info = requests.get(pay_info_url, auth=HTTPDigestAuth(op_id, psswd))
    pay_info = pay_info.json()

    url = 'http://' + addr + '/cgi/rep/pay'
    r = requests.get(url, auth=HTTPDigestAuth(op_id, psswd))
    if not check_error(r):
        res = []
        for item in r.json():
            name = None
            for info in pay_info:
                if item['no'] == info['id']:
                    name = info['Name']
            if name:
                item['name'] = name
            else:
                item['name'] = str(item['no'])
            res.append(item)

        for line in res:
            print("%s%s" % (
                (line['name'] + ':').ljust(10),
                line['sum'],
            ))
