from common import check_rms_edf

def edf_is_schedulable(tasks):
    """Check the task set schedulability for EDF.

    Check whether the specified task set is schedulable under EDF algorithm.

    :param tasks: list of task descriptors.

    :return: The return value. True for success, False otherwise.
    :rtype: bool.
    """

    totalUse = sum(task['exec_time'] for task in tasks)
    n = len(tasks)
    if(n == 0 ): return
    if(totalUse <= 1):
        return True
    else:
        return False

def edf(task_list, sim_time=0, verbose=False):
    """Simulates the Earliest Deadline First (EDF) scheduling algorithm.

    :param  task_list: List of task descriptors.
    :param sim_time: Time for simulation. If none is defined, then LCM (Lowest Common Multiple) of periods is used.
    :type  sim_time: int
    :param verbose:
    :type  verbose: bool

    :return: sched 
    :rtype: schedule list for each task (List of dictionaries)
    """

    if not check_rms_edf(task_list):
        print("Aborting execution of EDF algorithm due to invalid input file.")
        sys.exit(1)