from cmath import e
import pyhf
import numpy as np
import matplotlib.pyplot as plt
from pyhf.contrib.viz import brazil

pyhf.set_backend("numpy")


print("Setting up model.")

sig = {
    "name": "signal",
    "data": [6.0], #expected nominal signal
    "modifiers": [
        {
            "name": "mu", #multiplicative parameter for the signal x-section/strength
            "type": "normfactor",
            "data": None
        },
        {
            "name": "sys_sig_model",
            "type": "normsys",
            "data": {"hi": (1+0.2), "lo": (1-0.2)} #assigns a 20% relative uncertainty to the signal yield
        }
    ]
}

bkg = {
    "name": "background",
    "data": [9.0], # exoected background
    "modifiers": [
        {
            "name": "sys_bkg_model",
            "type": "normsys",
            "data": {"hi": (1+0.2), "lo": (1-0.2)} #assigns a 20% relative uncertainty to the background yield
        }
    ]   
}

channels = [
    {
        "name": "singlechannel",
        "samples": [sig, bkg]        
    }
]

measurements = [
    {
        "name": "measurement",
        "config": {
            "poi": "mu",
            "parameters": []
        }        
    }
]

observations = [
    {
        "name": "singlechannel",
        "data": [9.0]  #observed data (or set equal to expected)
    }
]

#build workspace
workspace = {
    "channels": channels,
    "observations": observations,
    "measurements": measurements,        
    "version": "1.0.0"
}

#get ws, model, data
ws = pyhf.Workspace(workspace)
model = ws.model()
data = ws.data(model)

#Alternative: simple model
#model = pyhf.simplemodels.uncorrelated_background(
#    signal=sig["data"], bkg=bkg["data"], bkg_uncertainty=[0.01]
#)
#data = observations[0]["data"] + model.config.auxdata

print("Calculating upper limits.")
scan_poi = np.linspace(0.01, 5, 41)
obs_limit, exp_limits = pyhf.infer.intervals.upperlimit(
    data, model, scan_poi, return_results=False)

print("======== RESULTS =========")
print(f"Observed limit on signal strength (mu): {obs_limit:.4f}")
exp_lim = exp_limits[2]
exp_lim_plus = exp_limits[3] - exp_lim
exp_lim_minus = exp_lim - exp_limits[1]
print(f"Expected limits on signal strength (mu): {exp_lim:.4f} +{exp_lim_plus:.4f} -{exp_lim_minus:.4f}")
