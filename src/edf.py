from common import check_rms_edf

def edf_is_schedulable(tasks):
    totalUse = sum(task['exec_time'] for task in tasks)
    n = len(tasks)
    if(n == 0 ): return
    if(totalUse <= 1):
        return True
    else:
        return False

def edf(task_list):

    if not check_rms_edf(task_list):
        print("Aborting execution of EDF algorithm due to invalid input file.")
        sys.exit(1)