This repository consists in tutorial examples to send jobs on the Ruby Machine at the TGCC.

The first_job_emulator do not call the QPU, eveything is run on one(s) of classical resources. The code is just taking one qubit from the state 0 to 1. As this job is done on an emulator with no noise, you can see that every run gives the same results (all 1000 shots are measured on state 1).  

The first_job_Ruby performs the same actions as first_job_emulator , taking a qubit from 0 to 1 as above, but with the modifications required to send it on the Ruby Machine. This script WILL send the job in the queue of the QPU and thus will consume a portion of your hour allocation on Ruby.

The TestQUBO is an adaptation of the tutorial found here https://docs.pasqal.com/pulser/tutorials/qubo/, that is sending this experiment to the QPU. This shows you a small nontrivial example of what kind of problem you can solve with Ruby. Similarly to above this script WILL send the job in the queue of the QPU and thus will consume a portion of your hour allocation on Ruby.

All these scripts have a version in .ipynb (jupyter notebook) and .py (python file) as you might need the first for visualisation/iteration, and the second for running it via command line in the TGCC environment. 
To convert a file from .ipynb to.py, use the command :
jupyter nbconvert --to python <file_name>.ipynb 


The SubScript is a shell that you can run with the command cc_msub in the TGCC environment. This allows you to submit a job to the QPU without tying its execution to your session.
This specific script is a shell to run first_job_Ruby.py, to be changed with another file name if you want to re-use it.
