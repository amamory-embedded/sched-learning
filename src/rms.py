from common import check_rms_edf, lcm
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
    #if not rms_is_schedulable(task_list):
    #    print("Aborting execution of RMS algorithm since this task set is not schedulable for RMS.")
    #    sys.exit(1)

    # Returns the LCM (Lowest Common Multiple) of a list of integers
    # this will determine the max simulation time
    list_period=[]
    for task in task_list:
        list_period.append(task['period'])
    task_lcm = np.lcm.reduce(list_period)
    print ("The simulation time is:", task_lcm)

    ready_list = []
    for task in task_list:
        #['name'],task['period'], task['deadline']
        # (computation time, task description)
        ready_list.append([task['exec_time'], task])

    print (ready_list)

    schedule = []
    for i in range(1,20):
        # check if there are tasks to be included in the ready_list
        for task in task_list:
            # check if it is time to start another job
            #print (i,task['period'])
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
        #print (ready_list)


    print (schedule)

    sched = {}
    sched['title'] = 'Some title'
    sched['sched'] = []
    print (sched)
    for task in task_list:
        sched_task = {}
        sched_task['name'] = task['name']
        sched_task['jobs'] = []
        print ("#############", task['name'], "#############")
        print (sched_task)
        #search for this task in the schedule
        for idx, ready_task in enumerate(schedule,start=1):
            if task['name'] == ready_task:
                start_time = idx
                if idx != len(schedule):
                    for idx2, ready_task2 in enumerate(schedule[idx:]):
                        end_time = idx+idx2
                        if task['name'] != ready_task2:
                            break
                else:
                    end_time = idx
                end_time +=1
                print (task['name'], "[",start_time,end_time,"]")
                sched_task['jobs'].append([start_time,end_time])
        print (sched_task)
        sched['sched'].append(sched_task)
        print ("##########################")
      #{'jobs': [], 'name': 'task1'}
    #print ("SCHED")
    #print (sched)
    return sched