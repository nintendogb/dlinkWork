import subprocess
import argparse
import json
import default_server

parser = argparse.ArgumentParser()
parser.add_argument(
    '-n',
    '--name',
    type=str,
    help='name of aws ec2 instance'
)
parser.add_argument(
    '-d',
    '--dir',
    type=str,
    help='save json location'
)
parser.add_argument(
    '--out_qaus321',
    dest='out_qaus321',
    action='store_true',
    default=False,
    help='region not in qaus321'
)
args = parser.parse_args()

def update_ins_name(cfg):
    for tag in cfg['TagSpecifications']:
        if tag['ResourceType'] == 'instance':
            tag['Tags'][0]['Value'] = args.name
        elif tag['ResourceType'] == 'volume':
            tag['Tags'][0]['Value'] = f'{args.name}_vol'

if args.out_qaus321:
    print('out_qaus321_cfg')
    def_cfg = eval(str(default_server.out_qaus321_cfg))
else:
    print('qaus321_cfg')
    def_cfg = eval(str(default_server.qaus321_cfg))

update_ins_name(def_cfg)
#print(json.dumps(def_cfg, indent=4))
print(f'{args.dir}/{args.name}.json')
with open(f'{args.dir}/{args.name}.json', 'w') as outfile:
    json.dump(def_cfg, outfile, indent=4)
