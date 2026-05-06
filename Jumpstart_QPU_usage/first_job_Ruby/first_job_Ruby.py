#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pulser
import matplotlib.pyplot as plt
import numpy as np
from pulser import InterpolatedWaveform, Pulse, QPUBackend, Sequence
from pulser.backend.remote import JobParams

from pulser_myqlm import PulserQLMConnection

# Connect to the QPU
conn = PulserQLMConnection()

# Get the Device implemented by the QPU from the QPU specs
FRESNEL_DEVICE = conn.fetch_available_devices()["qat.qpus:PasqalQPU"]

##Uncomment to have the specs of Ruby
#print("Using the Device:", "\n")
#FRESNEL_DEVICE.print_specs()

#Creation of the register. Note the use of the function with_automatic_layout.
register = pulser.Register.from_coordinates([(0, 0)], prefix="q").with_automatic_layout(FRESNEL_DEVICE)
register.draw()


sequence = pulser.Sequence(register, FRESNEL_DEVICE)



pi_pulse = pulser.Pulse.ConstantPulse(1000, np.pi, 0, 0)
sequence.add(pi_pulse, "rydberg_global")
sequence.draw(mode="input")


# In[ ]:


# Simulate the Sequence on the QPU
qpu = QPUBackend(sequence, connection=conn)

remote_results = qpu.run([JobParams(runs=10, variables=[])], wait=True)
count = remote_results[0].bitstring_counts


# In[2]:


# Creation of a text file with the results of your experiment. Will write over already existing test.txt file.

import json
with open("test.txt", "w") as f:
   json.dump(count,f)

    
## If you want to createa text file with a unique name tied to the job batch ID.
#id = remote_results.batch_id
#with open(f"{id}.txt", 'w') as f:
#    json.dump(count,f)

