import yaml
import argparse
import pprint
import os
import sys
import glob
import filecmp

#sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#
# from lib.Tasks import ManualTask, TaskMaster

# tests
# https://github.com/guilyx/gantt-trampoline/blob/master/tests/test_auto_tasks.py


# TODO: https://github.com/seperman/deepdiff to compare both YAMLs

#sys.path.insert(0, os.path.abspath('../src'))
sys.path.append('../src')
# supported algorithms
from rms import rms
from edf import edf

def main():
    """Tester for the scheduling algoritms. 

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
    pp = pprint.PrettyPrinter(indent=4)

    # set the tested scheduling algorithms and the testcases
    tested_sched_algo = ['rms','edf']
    testcases = glob.glob("testbench*.yaml")
   
    os.chdir("../examples")

    # main test loop
    for filename in testcases:
        # loading and parsing the input YAML file
        with open(filename) as f:
            try:
                docs = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)

        if args.verbose:
            print ('PRINTING THE INPUT CONFIGURATION FILE:')
            pp.pprint(docs)

        # testing the same file for different algorithms
        for algo in tested_sched_algo:
            print("Testing:",filename, algo)

            # loading and parsing the expected YAML file
            #dir_name = os.path.dirname(filename)
            extension = os.path.splitext(os.path.basename(filename))[1]
            fname = os.path.splitext(filename)[0]
            # if the filename is testbench2.yaml and the algorithm is RMS, then 
            # the output filename will be /tmp/testbench2-rms.yaml
            expected_file = "../tests/results/"+fname+"-"+algo+extension
            
            #is the expected results file is not found, it means that the 
            #taskset was not schedulable for this algo
            with open(expected_file) as f:
                try:
                    expected_doc = yaml.safe_load(f)
                except yaml.YAMLError as exc:
                    expected_doc = None
                    print("Expected results file is not found.", filename, "is not schedulable for", algo)

            # check wheter this yaml file support the selected algorithm
            valid_algo = False
            for supported_algo in docs['algo']:
                if supported_algo == algo:
                    valid_algo = True
                    break
            if not valid_algo:
                print ("ERROR: the selected file does not support the selected scheduling algorithm", algo)
                return 1

            # selecting and running the scheduling algorithm
            if algo == 'rms':
                sched = rms(docs['tasks'], verbose=args.verbose)
            elif algo == 'edf':
                sched = edf(docs['tasks'], verbose=args.verbose)
            else:
                print ("ERROR: unsupported scheduling algorithm", algo)
                return 1

            extension = os.path.splitext(filename)[1]
            fname = os.path.splitext(filename)[0]
            # if the filename is testbench2.yaml and the algorithm is RMS, then 
            # the output filename will be /tmp/testbench2-rms.yaml
            ofile = "/tmp/"+fname+"-"+algo+extension
            with open(ofile, 'w') as outfile:
                yaml.dump(sched, outfile, default_flow_style=False)

            #comparing the expected schedule with the obtained one
            if expected_doc != sched:
                print("ERROR:", filename, algo, "do not match")
            # compare both files
            if not filecmp.cmp(expected_file, ofile, shallow=False):
                print ('ERROR: PRINTING THE GENERATED FILES:')
                pp.pprint(expected_doc)
                pp.pprint(sched)
                return 1

    return 0

if __name__ == "__main__":
    main()
