#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pulser
from matplotlib import pyplot as plt

device = pulser.AnalogDevice
print(device.specs)

register = pulser.Register.from_coordinates([(0, 0)], prefix="q")
register.draw()

sequence = pulser.Sequence(register, device)

sequence.declare_channel("rydberg_global", "rydberg_global")
print(
    "The states used in the computation are", sequence.get_addressed_states()
)

pi_pulse = pulser.Pulse.ConstantPulse(1000, np.pi, 0, 0)
sequence.add(pi_pulse, "rydberg_global")
sequence.draw(mode="input")

backend = pulser.backends.QutipBackendV2(sequence)
result = backend.run()

count = result.final_bitstrings

print(count)







