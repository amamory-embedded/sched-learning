from common import check_rms_edf, lcm
import numpy as np

def rms(task_list):
    """Simulates the Rate Monotonic (RM) scheduling algorithm

    Args:
        task_list: list of task descriptors

    Returns:
        int: the LCM
    """

    if not check_rms_edf(task_list):
        print("Aborting execution of RMS algorithm due to invalid input file.")
        sys.exit(1)
    
    # Returns the LCM (Lowest Common Multiple) of a list of integers
    # this will determine the max simulation time
    list_period=[]
    for task in task_list:
        list_period.append(task['period'])
    task_lcm = np.lcm.reduce(list_period)
    print ("The simulation time is:", task_lcm)
    

    #for i in range(task_lcm):

      