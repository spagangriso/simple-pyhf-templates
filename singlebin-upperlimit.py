from cmath import e
import pyhf
import numpy as np
import matplotlib.pyplot as plt
from pyhf.contrib.viz import brazil

pyhf.set_backend("numpy")


print("Setting up model.")

sig = {
    "name": "signal",
    "data": [6.0],
    "modifiers": [
        {
            "name": "mu",
            "type": "normfactor",
            "data": None
        },
        {
            "name": "sys_sig_model",
            "type": "normsys",
            "data": {"hi": (1+0.2), "lo": (1-0.2)}
        }
    ]
}

bkg = {
    "name": "background",
    "data": [9.0],
    "modifiers": [
        {
            "name": "sys_bkg_model",
            "type": "normsys",
            "data": {"hi": (1+0.2), "lo": (1-0.2)}
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
        "data": [9.0]        
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
print(f"Observed limit: {obs_limit:.4f}")
exp_lim = exp_limits[2]
exp_lim_plus = exp_limits[3] - exp_lim
exp_lim_minus = exp_lim - exp_limits[1]
print(f"Expected limits: {exp_lim:.4f} +{exp_lim_plus:.4f} -{exp_lim_minus:.4f}")
