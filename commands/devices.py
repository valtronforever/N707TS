import json
from lib.ssdp import get_available_devices


def run(cmd_args=None):
    if not cmd_args.json:
        print('Searching...')
    devices = get_available_devices()
    if cmd_args.json:
        dev_list = [{
            'ip': x[0],
            'model': x[1],
            'serial': x[2],
        } for x in devices]
        print(json.dumps({
            'result': 'ok',
            'response': dev_list,
        }))
    else:
        print("%s | %s | %s |" % (
            'IP'.ljust(15),
            'Model'.ljust(15),
            'Serial'.ljust(15),
        ))
        print('-' * 53)
        for dev in devices:
            print("%s | %s | %s" % (
                dev[0].ljust(15),
                dev[1].ljust(15),
                dev[2].ljust(15),
            ))
