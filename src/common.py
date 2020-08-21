
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


from math import gcd
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

from datetime import datetime
def convert_to_datetime(x):
    """Auxiliar function used to plot the gantt chart

    Args:
        x: interger value

    Returns:
        date_time
    """
    return datetime.fromtimestamp(31536000+x*24*3600).strftime("%Y-%d-%m")

import plotly.express as px
import pandas as pd
import numpy as np
def plot_gantt():
    """Use the plotly lib to plot the gantt chart
    based on: https://stackoverflow.com/questions/57686684/using-numerical-values-in-plotly-for-creating-gantt-charts

    Args:
        sched: schedule list for each task

    Returns:
        None
    """



    df = pd.DataFrame([
        dict(Task="Job A", Start=convert_to_datetime(1), Finish=convert_to_datetime(3)),
        dict(Task="Job A", Start=convert_to_datetime(4), Finish=convert_to_datetime(5)),
        dict(Task="Job C", Start=convert_to_datetime(2), Finish=convert_to_datetime(6))
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up

    num_tick_labels = np.linspace(start = 0, stop = 10, num = 11, dtype = int)
    date_ticks = [convert_to_datetime(x) for x in num_tick_labels]
    fig.layout.xaxis.update({
            'tickvals' : date_ticks,
            'ticktext' : num_tick_labels
            })
    fig.show()