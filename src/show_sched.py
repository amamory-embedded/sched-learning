import yaml
import argparse
import pprint
import sys
# supported algorithms 
from rms import rms
from common import plot_gantt, check_sched

def main(file_name):
    """Show the schedule image of a shedule YAML file. 

    Example of schedule image:

    .. image:: ../../wikipedia.png

    :param file_name: The shedule YAML file.
    :type  file_name: List of dictionaries.
    :return: None.
    """

    # loading and parsing the YAML file
    with open(file_name) as f:
        docs = yaml.load(f, Loader=yaml.FullLoader)

    if args.verbose:
        print ('PRINTING THE INPUT SCHEDULING FILE:')
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(docs)

    plot_gantt(docs, verbose=args.verbose)

if __name__ == "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('--verbose', dest='verbose', action='store_true', default=False)

    args = parser.parse_args()

    main()
