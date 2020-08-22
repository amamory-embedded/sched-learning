Welcome to YATSS's documentation!
=========================================================================


.. toctree::
   :maxdepth: 2
   :caption: Contents:


YATSS (Yet Another Task Scheduling Simulator).
Supported task scheduling algorithms: 

* `Rate Monotonic Scheduling (RMS) algorithm <https://en.wikipedia.org/wiki/Rate-monotonic_scheduling>`_;
* `Earliest Deadline First (EDF) algorithm <https://en.wikipedia.org/wiki/Earliest_deadline_first_scheduling>`_.

Creating the conda environment
==============================

::

    conda create --name yatss python=3.6
    conda activate yatss
    conda install pandas
    conda install pyyaml
    conda install plotly
    conda install sphinx
    pip install sphinx-rtd-theme
    pip install sphinx-autodoc

Installing and running
======================

::

    git clone 
    cd shed-learning
    python src/main.py example/testbench2.yaml

Docs
====



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


