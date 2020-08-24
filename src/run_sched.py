import yaml
import argparse
import pprint
import sys
# supported algorithms
from rms import rms
from edf import edf
from common import plot_gantt

def main():
    """Executes a task scheduling for a givin algorithm. 

    Given an input file describing the task set, this function generates
     its scheduling considering the scheduling algorithm passed by argument.
     At the end, it generates a schedule image, similar to this one: 

    .. image:: ../../wikipedia.png

    :param file_name: The shedule YAML file.
    :type  file_name: List of dictionaries.
    :return: None.
    """
    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'),
                        help='input file describing the tasks to be scheduled'
                        )
    parser.add_argument('--ofile', type=argparse.FileType('w'),
                        help='output file with the resulting schedule. If not defined, it will not be saved in a file'
                        )
    parser.add_argument('-s','--simtime', dest='sim_time', default=0, type=int,
                help='The number of OS ticks to be simulated.')
    parser.add_argument('-v','--verbose', dest='verbose', action='store_true', default=False)
    parser.add_argument('--sched',
                        default='rms',
                        nargs='?',
                        choices=['rms', 'edf'],
                        help='list of supported task scheduling algoritms (default: %(default)s)')

    args = parser.parse_args()

    # loading and parsing the YAML file
    with open(args.file.name) as f:
        try:
            docs = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    pp = pprint.PrettyPrinter(indent=4)
    if args.verbose:
        print ('PRINTING THE INPUT CONFIGURATION FILE:')
        pp.pprint(docs)

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
        sched = rms(docs['tasks'], sim_time=args.sim_time, verbose=args.verbose)
    elif args.sched == 'edf':
        sched = edf(docs['tasks'], sim_time=args.sim_time, verbose=args.verbose)
    else:
        print ("ERROR: unsupported scheduling algorithm", args.sched)
        sys.exit(1)

    if args.verbose:
        print ('PRINTING THE GENERATED SCHEDULING FILE:')
        pp.pprint(sched)

    if args.ofile is not None:
        with open(args.ofile.name, 'w') as outfile:
            yaml.dump(sched, outfile, default_flow_style=False)

    plot_gantt(sched, verbose=args.verbose)

    return sched

if __name__ == "__main__":
    main()
