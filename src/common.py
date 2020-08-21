import sys
from math import gcd
from datetime import datetime
# for plotting
import plotly.express as px
import pandas as pd
import numpy as np


def versiontuple(v):
    """Convert a string of package version in a tuple for future comparison

    Args:
        version : string version, e.g "2.3.1"

    Usage: 
        >> versiontuple("2.3.1") > versiontuple("10.1.1")
        False

    Returns:
        bool: The return tuple, e.g. (2,3,1)
    """    
    return tuple(map(int, (v.split("."))))


def check_rms_edf(task_list):
    """Parse the YAML for the required field for RMS and EDF algorithms

    Args:
        task_list: list of task descriptors

    Returns:
        bool: The return value. True for success, False otherwise.
    """
    
    ##############
    # validate the input format first. some fields are expected for rms
    ##############

    # must have at least 2 tasks
    if len(task_list) <= 1:
        print ("ERROR: the task list must have more than 1 task. Found", len(task_list))
        return False

    # check if all tasks have the mandatory fields
    print ('checking the task list ... ', end='')
    for task in task_list:
        if 'name' not in task:
            print ("\nERROR: field 'name' not found in task")
            return False
        if 'exec_time' not in task:
            print ("\nERROR: field 'exec_time' not found in task")
            return False
        if 'period' not in task:
            print ("\nERROR: field 'period' not found in task")
            return False
        if 'deadline' not in task:
            print ("\nERROR: field 'deadline' not found in task")
            return False
 
    # each task must have a name (str), exec_time (N), deadline (N), period (N)
    for task in task_list:
        if type(task['name']) is not str:
            print ("\nERROR: string expected in the 'name' field. Got",type(task['name']))
            return False
        if type(task['exec_time']) is not int:
            print ("\nERROR: int expected in the 'exec_time' field. Got",type(task['exec_time']))
            return False
        if task['exec_time'] <= 0:
            print ("\nERROR: 'exec_time' field must be a positive integer. Got",task['exec_time'])
            return False
        if type(task['period']) is not int:
            print ("\nERROR: int expected in the 'period' field. Got",type(task['period']))
            return False
        if task['period'] <= 0:
            print ("\nERROR: 'period' field must be a positive integer. Got",task['period'])
            return False
        if type(task['deadline']) is not int:
            print ("\nERROR: int expected in the 'deadline' field. Got",type(task['deadline']))
            return False
        if task['deadline'] <= 0:
            print ("\nERROR: 'deadline' field must be a positive integer. Got",task['deadline'])
            return False

    print ('passed !')  
    return True  



def check_sched(sched):
    """Parse the YAML for the resulting schedule of a scheduling algorithm

    Args:
        sche: list of sched descriptors

    Returns:
        bool: The return value. True for success, False otherwise.
    """
    
    ##############
    # validate the input format first. some fields are expected for rms
    ##############

    # must have at least 1 task
    if len(sched['sched']) < 1:
        print ("ERROR: the sched list must have at least 1 task. Found", len(sched['sched']))
        return False

    # check if all tasks have the mandatory fields
    print ('checking the scheduling list ... ', end='')
    for task in sched['sched']:
        if 'name' not in task:
            print ("\nERROR: field 'name' not found in task")
            return False
        if 'jobs' not in task:
            print ("\nERROR: field 'jobs' not found in task")
            return False
        if len(task['jobs']) <= 0:
            print ("\nERROR: a task must have at least one job. Got", len(task['jobs']))
            return False
        for job in task['jobs']:
            if type(job[0]) is not int or type(job[1]) is not int:
                print ("\nERROR: jobs must be int initial and final times. Got", type(job[0]), type(job[1]))
                return False
            if job[0] >= job[1]:
                print ("\nERROR: the initial job time must be lower than the the final time. Got", job[0], job[1])
                return False
            # zero is not supported in the plotting function
            if job[0] > 0:
                print ("\nERROR: the initial job time must be greater than 0. Got", job[0])
                return False
            if job[1] > 0:
                print ("\nERROR: the initial job time must be greater than 0. Got", job[1])
                return False

    print ('passed !')  
    return True  



def lcm (int_list):
    """Returns the LCM (Lowest Common Multiple) of a list of integers
    source: https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python

    Args:
        int_list: list of positive integers

    Returns:
        int: the LCM
    """
    if len(int_list) > 0:
        lcm = int_list[0]
        for i in int_list[1:]:
            lcm = lcm*i/gcd(lcm, i)
        return lcm
    else:
        return -1


def convert_to_datetime(x):
    """Auxiliar function used to plot the gantt chart

    Args:
        x: interger value

    Returns:
        date_time
    """

    #data_conv = datetime.fromtimestamp(31536000+x*24*3600).strftime("%Y-%d-%m")
    #print (data_conv)
    #return data_conv
    return datetime.fromtimestamp(31536000+x*24*3600).strftime("%Y-%d-%m")



def plot_gantt(sched):
    """Use the plotly lib to plot the gantt chart
    based on: https://stackoverflow.com/questions/57686684/using-numerical-values-in-plotly-for-creating-gantt-charts

    Args:
        sched: schedule list for each task

        sched example in python format:
        {   'sched': [  {'jobs': [[0, 3], [5, 7]], 'name': 'task1'},
                        {'jobs': [[4, 6]], 'name': 'task2'},
                        {'jobs': [[3, 4]], 'name': 'task3'}]}
        
        sched example in YAML:
            sched:
                - name: task1
                    jobs: 
                    - [0, 3]
                    - [5, 7]
                - name: task2
                    jobs: 
                    - [4,6]
                - name: task3
                    jobs: 
                    - [3,4]

    Returns:
        None
    """

    # check plotly version
    if versiontuple(px.__version__) < versiontuple("4.9.0"):
        print ("ERROR: the scheduling plotting function requires plotly 4.9.0 or newer. Found", px.__version__)
        return False

    # check the input argument
    if not check_sched(sched):
        print("Aborting execution of scheduling plotting due to invalid input file.")
        sys.exit(1)

    # create the data format required by pandas DataFrame
    list_tasks = []
    for task in sched['sched']:
        for job in task['jobs']:
            list_tasks.append(dict(Task=task['name'], Start=convert_to_datetime(job[0]), Finish=convert_to_datetime(job[1])))

    #list_tasks.append(dict(Task="Job A", Start=convert_to_datetime(1), Finish=convert_to_datetime(3)))
    #list_tasks.append(dict(Task="Job A", Start=convert_to_datetime(5), Finish=convert_to_datetime(7)))
    #list_tasks.append(dict(Task="Job B", Start=convert_to_datetime(4), Finish=convert_to_datetime(6)))
    #list_tasks.append(dict(Task="Job C", Start=convert_to_datetime(3), Finish=convert_to_datetime(4)))

    #list_tasks.append(dict(Task="Job A", Start=convert_to_datetime(1), Finish=convert_to_datetime(3)))
    #list_tasks.append(dict(Task="Job A", Start=convert_to_datetime(4), Finish=convert_to_datetime(5)))
    #list_tasks.append(dict(Task="Job C", Start=convert_to_datetime(2), Finish=convert_to_datetime(6)))

    #df = pd.DataFrame([
    #    dict(Task="Job A", Start=convert_to_datetime(1), Finish=convert_to_datetime(3)),
    #    dict(Task="Job A", Start=convert_to_datetime(4), Finish=convert_to_datetime(5)),
    #    dict(Task="Job C", Start=convert_to_datetime(2), Finish=convert_to_datetime(6))
    #])
    #print (list_tasks)

    df = pd.DataFrame(list_tasks)

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up

    num_tick_labels = np.linspace(start = 0, stop = 10, num = 11, dtype = int)
    date_ticks = [convert_to_datetime(x) for x in num_tick_labels]
    fig.layout.xaxis.update({
            'tickvals' : date_ticks,
            'ticktext' : num_tick_labels
            })
    fig.show()