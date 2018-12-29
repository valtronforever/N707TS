import requests
import json
from requests.auth import HTTPDigestAuth
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, print_timeout, cmd_args=None):
    pay_info_url = 'http://' + addr + '/cgi/tbl/Pay'
    pay_info = requests.get(pay_info_url, auth=HTTPDigestAuth(op_id, psswd), timeout=timeout)
    pay_info = pay_info.json()

    url = 'http://' + addr + '/cgi/rep/pay'
    r = requests.get(url, auth=HTTPDigestAuth(op_id, psswd), timeout=timeout)
    if not check_error(r, json_out=cmd_args.json):
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

        if cmd_args.json:
            print(json.dumps({
                'result': 'ok',
                'response': res,
            }))
        else:
            for line in res:
                print("%s%s" % (
                    (line['name'] + ':').ljust(10),
                    line['sum'],
                ))
