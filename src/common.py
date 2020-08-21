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

    Supported task_list in Python format:
    {   'algo': ['edf', 'rms'],
        'tasks': [   {   'deadline': 135,
                        'exec_time': 45,
                        'name': 'task1',
                        'period': 135},
                    {   'deadline': 150,
                        'exec_time': 50,
                        'name': 'task2',
                        'period': 150},
                    {   'deadline': 360,
                        'exec_time': 80,
                        'name': 'task3',
                        'period': 360}]}

    Supported task_list in YAML format:
    algo: 
    - edf
    - rms
    tasks:
    - name: task1
        exec_time: 45
        deadline: 135
        period: 135
    - name: task2
        exec_time: 50
        deadline: 150
        period: 150
    - name: task3
        exec_time: 80
        deadline: 360
        period: 360    

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
            if job[0] <= 0:
                print ("\nERROR: the initial job time must be greater than 0. Got", job[0])
                return False
            if job[1] <= 0:
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
    https://plotly.com/python/gantt/
    https://plotly.com/python-api-reference/generated/plotly.express.timeline.html
    https://plotly.com/python-api-reference/generated/plotly.graph_objects.html#plotly.graph_objects.Figure

    TODO: add a slider
    https://plotly.com/python/animations/
    https://plotly.com/python/sliders/

    TODO: provide an alternative plotting option with matplotlib
    https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/broken_barh.html

    TODO: other alternative plots
    https://github.com/ehsan-elwan/RM-Task-Scheduling/blob/master/Plotter.py
    https://github.com/johnharakas/scheduling-des/blob/sim-plotting/Qt_Canvas.py
    https://github.com/esalehi1996/Realtime_Scheduling_python/blob/master/main.py
    https://github.com/carlosgeos/uniprocessor-scheduler/blob/master/src/simulation.py
    https://github.com/ksameersrk/rt-scheduler/blob/master/analysis/plot_graph.py
    https://github.com/guilyx/gantt-trampoline/blob/master/lib/GanttPlot.py

    TODO: export figure with the plot
    https://plotly.com/python/static-image-export/

    Args:
        sched: schedule list for each task

        sched example in python format:
        {   'sched': [   {'color': 'yellow', 'jobs': [[1, 3], [5, 7]], 'name': 'task1'},
                        {'color': 'green', 'jobs': [[4, 6]], 'name': 'task2'},
                        {'jobs': [[3, 4]], 'name': 'task3'}],
            'title': 'scheduling with RMS'}
        
        sched example in YAML:
            title: "scheduling with RMS"
            sched:
                - name: task1
                  color: 'yellow'
                  jobs: 
                    - [1, 3]
                    - [5, 7]
                - name: task2
                  color: 'green'
                  jobs: 
                    - [4,6]
                - name: task3
                    jobs: 
                    - [3,4]
        The fields 'title' and 'color' are optional.

    Returns:
        None
    """

    # check plotly version
    import plotly as pl
    #print (pl.__version__)
    if versiontuple(pl.__version__) < versiontuple("4.9.0"):
        print ("ERROR: the scheduling plotting function requires plotly 4.9.0 or newer. Found", pl.__version__)
        return False

    # check the input argument
    if not check_sched(sched):
        print("Aborting execution of scheduling plotting due to invalid input file.")
        sys.exit(1)

    # create the data format required by pandas DataFrame
    list_tasks = []
    for task in sched['sched']:
        # color is not mandatory for a task
        if 'color' in  task:
            task_color = task['color']
        else:
            task_color = 'blue' # the default color
        
        for job in task['jobs']:
            list_tasks.append(dict(Task=task['name'], Start=convert_to_datetime(job[0]), Finish=convert_to_datetime(job[1]), Color = task_color))

    # creating the pandas DataFrame requred by plotly
    df = pd.DataFrame(list_tasks)

    # title is optional
    if 'title' in  sched:
        chart_title = sched['title']
    else:
        chart_title = ''

    fig = px.timeline(df, title = chart_title, x_start="Start", x_end="Finish", color = "Color", y="Task")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up

    # this part converts dates into ticks
    num_tick_labels = np.linspace(start = 0, stop = 10, num = 11, dtype = int)
    date_ticks = [convert_to_datetime(x) for x in num_tick_labels]
    fig.layout.xaxis.update({
            'tickvals' : date_ticks,
            'ticktext' : num_tick_labels
            })

    # it will show in the browser
    fig.show()