import requests
import json
from requests.auth import HTTPDigestAuth
from configparser import ConfigParser
from utils.errors import check_error


def run(addr, op_id, psswd, timeout, cmd_args=None):
    url = 'http://' + addr + '/cgi/tbl/Oper'

    # Request only as service
    r = requests.get(url, auth=HTTPDigestAuth('service', '751426'), timeout=timeout)
    if not check_error(r, json_out=cmd_args.json):
        if getattr(cmd_args, 'service', False):
            config = ConfigParser()
            config.read('config.ini')
            config['DEFAULT']['op_id'] = 'service'
            config['DEFAULT']['op_psswd'] = '751426'

            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            if cmd_args.json:
                print(json.dumps({'result': 'ok'}))
            else:
                print('OK')
        elif getattr(cmd_args, 'set', False):
            for oper in r.json():
                if str(oper['id']) == str(cmd_args.set):
                    config = ConfigParser()
                    config.read('config.ini')
                    config['DEFAULT']['op_id'] = str(oper['id'])
                    config['DEFAULT']['op_psswd'] = str(oper['Pswd'])

                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
                    if cmd_args.json:
                        print(json.dumps({'result': 'ok'}))
                    else:
                        print('OK')
                    return
            if cmd_args.json:
                print(json.dumps({
                    'result': 'error',
                    'message': 'No operator found with given id %s' % str(cmd_args.set),
                }))
            else:
                print('No operator found with given id %s' % str(cmd_args.set))
        else:
            if cmd_args.json:
                print(json.dumps({
                    'result': 'ok',
                    'response': r.json(),
                }))
            else:
                print("%s | %s | %s |" % (
                    'Id'.ljust(3),
                    'Name'.ljust(32),
                    'Password'.ljust(10),
                ))
                print('-'*53)
                for oper in r.json():
                    print("%s | %s | %s" % (
                        str(oper['id']).rjust(3),
                        oper['Name'].ljust(32),
                        str(oper['Pswd']).ljust(32),
                    ))
