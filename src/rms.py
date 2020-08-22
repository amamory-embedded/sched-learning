from common import check_rms_edf, sched_list_2_sched_dict
import numpy as np
import sys


def rms_is_schedulable(tasks):
    """Check whether the specified task set is schedulable under RMS algorithm

    Args:
        task_list: list of task descriptors

    Returns:
        bool: The return value. True for success, False otherwise.
    """

    totalUse = sum(task['exec_time']/float(task['period']) for task in tasks)
    n = len(tasks)
    if(n == 0 ): return
    #check scallability based off of total use and number os tasks
    print ("RMS schedudability",totalUse, " <= ", n*(2**(1/n)-1))
    if (totalUse <= n*(2**(1/n)-1)):
        return True
    else:
        return False
       

def rms(task_list, sim_time=0, verbose=False):
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
    #if not rms_is_schedulable(task_list):
    #    print("Aborting execution of RMS algorithm since this task set is not schedulable for RMS.")
    #    sys.exit(1)

    # if the simulation time is not specified by the user, then use the LCM of the task periods
    if sim_time == 0:
        # Returns the LCM (Lowest Common Multiple) of a list of integers
        # this will determine the max simulation time
        list_period=[]
        for task in task_list:
            list_period.append(task['period'])
        sim_time = np.lcm.reduce(list_period)
        
    print ("The simulation time is:", sim_time)

    # assuming all the tasks start at time zero, initialize the OS's ready_list
    ready_list = []
    for task in task_list:
        ready_list.append([task['exec_time'], task])
    #print (ready_list)

    schedule = []
    for i in range(1,sim_time+1):
        # check if there are tasks to be included in the ready_list
        for task in task_list:
            # check if it is time to start another job
            if ((i % task['period']) == 0):
                ready_list.append([task['exec_time'], task])
        # shortest period first
        ready_list.sort(key=lambda x: x[1]['period'], reverse=False)

        if len(ready_list) ==0:
            schedule.append('idle')
            # skip this OS tick
            continue
        # top task gain access to the cpu
        schedule.append(ready_list[0][1]['name'])
        # decrement computation time of the top job
        ready_list[0][0] -= 1
        # check if there are jobs to be included in the ready_list
        for job in ready_list:
            # check if the job finished, then delete the top of the list
            if job[0] == 0:
               del ready_list[0]

    #print (schedule)

    # artificially including a new task called idle to track the CPU idle time
    task_list.append(
        dict(
            name= 'idle',
            exec_time= 1,
            deadline= 1,
            period= 1,
        )
    )

    sched = sched_list_2_sched_dict(task_list,schedule,verbose)

    return sched