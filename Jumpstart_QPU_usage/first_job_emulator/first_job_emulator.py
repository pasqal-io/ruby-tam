#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pulser
from matplotlib import pyplot as plt


#selection of the backend
device = pulser.AnalogDevice



#Register
register = pulser.Register.from_coordinates([(0, 0)], prefix="q")
register.draw()

sequence = pulser.Sequence(register, device)


#Pulse Shaping
sequence.declare_channel("rydberg_global", "rydberg_global")

pi_pulse = pulser.Pulse.ConstantPulse(1000, np.pi, 0, 0)
sequence.add(pi_pulse, "rydberg_global")
sequence.draw(mode="input")


# In[ ]:


#Execution of the sequence
backend = pulser.backends.QutipBackendV2(sequence)
result = backend.run()

count = result.final_bitstrings

print(count)


# In[ ]:


# Creation of a text file with the results of your experiment. Will write over already existing test.txt file.

import json
with open("test.txt", "w") as f:
   json.dump(count,f)

    
## If you want to createa text file with a unique name tied to the job batch ID.
#id = remote_results.batch_id
#with open(f"{id}.txt", 'w') as f:
#    json.dump(count,f)


# In[ ]:




