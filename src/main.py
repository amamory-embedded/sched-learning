import yaml
import argparse
import pprint
import sys
# supported algorithms
from rms import rms
from common import plot_gantt

# parsing arguments

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('--sched',
                    default='rms',
                    nargs='?',
                    choices=['rms', 'edf'],
                    help='list of supported task scheduling algoritms (default: %(default)s)')

args = parser.parse_args()

# loading and parsing the YAML file
with open(args.file.name) as f:
    docs = yaml.load(f, Loader=yaml.FullLoader)

print ('PRINTING THE INPUT CONFIGURATION FILE:')
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(docs)

#pp.pprint(docs['algo'][0])
#pp.pprint(docs['tasks'][0]['name'])

# check wheter this yaml file support the selected algorithm

valid_algo = False
for algo in docs['algo']:
    if algo == args.sched:
        valid_algo = True
        break

if not valid_algo:
    print ("ERROR: the selected file does not support the selected scheduling algorithm",args.sched)
    sys.exit(1)


# selecting and running the scheduling algorithm
if args.sched == 'rms':
    sched = rms(docs['tasks'])
elif args.sched == 'edf':
    sched = edf(docs['tasks'])
else:
    print ("ERROR: unsupported scheduling algorithm", args.sched)
    sys.exit(1)

# loading and parsing the YAML file
with open('examples/sched2.yaml') as f:
    sched = yaml.load(f, Loader=yaml.FullLoader)

print ('PRINTING THE GENERATED SCHEDULING FILE:')
pp.pprint(sched)

plot_gantt(sched)


