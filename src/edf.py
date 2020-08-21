from common import check_rms_edf

def edf(task_list):

    if not check_rms_edf(task_list):
        print("Aborting execution of EDF algorithm due to invalid input file.")
        sys.exit(1)