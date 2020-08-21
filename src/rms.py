from common import check_rms_edf, lcm
import numpy as np


def rms_is_schedulable(tasks):
    """Check whether the specified task set is schedulable under RMS algorithm

    Args:
        task_list: list of task descriptors

    Returns:
        bool: The return value. True for success, False otherwise.
    """

    totalUse = sum(task['exec_time'] for task in tasks)
    n = len(tasks)
    if(n == 0 ): return
    #check scallability based off of total use and number os tasks
    if (totalUse <= n*(2**(1/n)-1)):
        return True
    else:
        return False
       

def rms(task_list):
    """Simulates the Rate Monotonic (RM) scheduling algorithm

    Args:
        task_list: list of task descriptors

    Returns:
        sched: schedule list for each task
    """

    # check the input syntax
    if not check_rms_edf(task_list):
        print("Aborting execution of RMS algorithm due to invalid input file.")
        sys.exit(1)
    
    # check schedulability of the task set
    if not rms_is_schedulable(task_list):
        print("Aborting execution of RMS algorithm since this task set is not schedulable.")
        sys.exit(1)

    # Returns the LCM (Lowest Common Multiple) of a list of integers
    # this will determine the max simulation time
    list_period=[]
    for task in task_list:
        list_period.append(task['period'])
    task_lcm = np.lcm.reduce(list_period)
    print ("The simulation time is:", task_lcm)


    #for i in range(task_lcm):

      