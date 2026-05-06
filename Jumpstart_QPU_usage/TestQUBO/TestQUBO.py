#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pulser
import pulser_simulation
from scipy.optimize import minimize
from scipy.spatial.distance import pdist, squareform


# In[ ]:


Q = np.array(
    [
        [-10.0, 19.7365809, 19.7365809, 5.42015853, 5.42015853],
        [19.7365809, -10.0, 20.67626392, 0.17675796, 0.85604541],
        [19.7365809, 20.67626392, -10.0, 0.85604541, 0.17675796],
        [5.42015853, 0.17675796, 0.85604541, -10.0, 0.32306662],
        [5.42015853, 0.85604541, 0.17675796, 0.32306662, -10.0],
    ]
)


# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from pulser import InterpolatedWaveform, Pulse, QPUBackend, Sequence
from pulser.backend.remote import JobParams

from pulser_myqlm import PulserQLMConnection

# Connect to the QPU
conn = PulserQLMConnection()

# Get the Device implemented by the QPU from the QPU specs
FRESNEL_DEVICE = conn.fetch_available_devices()["qat.qpus:PasqalQPU"]
#print("Using the Device:", "\n")
#FRESNEL_DEVICE.print_specs()


# In[ ]:


def evaluate_mapping(
    new_coords: np.ndarray, Q: np.ndarray, device: FRESNEL_DEVICE
):
    """Cost function to minimize. Ideally, the pairwise distances are conserved."""
    new_coords = np.reshape(new_coords, (len(Q), 2))
    # computing the matrix of the distances between all coordinate pairs
    new_Q = squareform(device.interaction_coeff / pdist(new_coords) ** 6)
    return np.linalg.norm(new_Q - Q)


# In[ ]:


costs = []
np.random.seed(0)
x0 = np.random.random(len(Q) * 2)
res = minimize(
    evaluate_mapping,
    x0,
    args=(Q, FRESNEL_DEVICE),
    method="Nelder-Mead",
    tol=1e-6,
    options={"maxiter": 200000, "maxfev": None},
)
coords = np.reshape(res.x, (len(Q), 2))


# In[ ]:


qubits = {f"q{i}": coord for (i, coord) in enumerate(coords)}
reg = pulser.Register(qubits).with_automatic_layout(FRESNEL_DEVICE)
reg.draw(
    blockade_radius=FRESNEL_DEVICE.rydberg_blockade_radius(1.0),
    draw_graph=False,
    draw_half_radius=True,
    draw_empty_sites=True
)


# In[ ]:


sequence = pulser.Sequence(reg, FRESNEL_DEVICE)


# In[ ]:


sequence.declare_channel("rydberg_global", "rydberg_global")


# In[ ]:


# We choose a median value between the min and the max
Omega = np.median(Q[Q > 0].flatten())
delta_0 = -5  # just has to be negative
delta_f = -delta_0  # just has to be positive
T = 4000  # time in ns, we choose a time long enough to ensure the propagation of information in the system


# In[ ]:


adiabatic_pulse = pulser.Pulse(
    pulser.InterpolatedWaveform(T, [1e-9, Omega, 1e-9]),
    pulser.InterpolatedWaveform(T, [delta_0, 0, delta_f]),
    0,
)
sequence.add(adiabatic_pulse, "rydberg_global")
sequence.draw()


# In[ ]:


# Simulate the Sequence on the QPU
qpu = QPUBackend(sequence, connection=conn)

remote_results = qpu.run([JobParams(runs=10, variables=[])], wait=True)
count = remote_results[0].bitstring_counts


# In[ ]:


print(count)


# In[ ]:


import json
with open("test.txt", "w") as f:
   json.dump(count,f)


# In[ ]:




