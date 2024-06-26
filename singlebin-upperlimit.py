from cmath import e
import pyhf
import numpy as np
import matplotlib.pyplot as plt
from pyhf.contrib.viz import brazil

pyhf.set_backend("numpy")

#######################################################################################
from pyhf.infer import hypotest
from pyhf import get_backend
def _interp(x, xp, fp):
    tb, _ = get_backend()
    return tb.astensor(np.interp(x, xp.tolist(), fp.tolist()))

def local_upperlimit(data, model, scan, level=0.05, return_results=False, **hypotest_kwargs):
    """
    Calculate an upper limit interval ``(0, poi_up)`` for a single
    Parameter of Interest (POI) using a fixed scan through POI-space.
    """
    tb, _ = get_backend()
    results = [
        hypotest(mu, data, model, return_expected_set=True, **hypotest_kwargs)
        for mu in scan
    ]
    obs = tb.astensor([[r[0]] for r in results])
    exp = tb.astensor([[r[1][idx] for idx in range(5)] for r in results])

    result_arrary = tb.concatenate([obs, exp], axis=1).T

    # observed limit and the (0, +-1, +-2)sigma expected limits
    limits = [_interp(level, result_arrary[idx][::-1], scan[::-1]) for idx in range(6)]
    obs_limit, exp_limits = limits[0], limits[1:]

    if return_results:
        return obs_limit, exp_limits, (scan, results)
    return obs_limit, exp_limits
#######################################################################################

print("Setting up model.")

sig = {
    "name": "signal",
    "data": [1.0], #expected nominal signal
    "modifiers": [
        {
            "name": "mu", #multiplicative parameter for the signal x-section/strength
            "type": "normfactor",
            "data": None
        },
        {
            "name": "sys_sig_model",
            "type": "normsys",
            "data": {"hi": (1+0.01), "lo": (1-0.01)} #assigns a 1% (small) relative uncertainty to the signal yield
        }
    ]
}

bkg = {
    "name": "background",
    "data": [0.05], # exoected background
    "modifiers": [
        {
            "name": "sys_bkg_model",
            "type": "normsys",
            "data": {"hi": (1+0.02), "lo": (1-0.02)} #assigns a 2% relative uncertainty to the background yield
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
        "data": [0.0]  #observed data (or set equal to expected)
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
#obs_limit, exp_limits = pyhf.infer.intervals.upperlimit(
obs_limit, exp_limits = local_upperlimit(
    data, model, scan_poi, return_results=False, 
        test_stat="qtilde", calctype='toybased', ntoys=100)

print("======== RESULTS =========")
print(f"Observed limit on signal strength (mu): {obs_limit:.4f}")
exp_lim = exp_limits[2]
exp_lim_plus = exp_limits[3] - exp_lim
exp_lim_minus = exp_lim - exp_limits[1]
print(f"Expected limits on signal strength (mu): {exp_lim:.4f} +{exp_lim_plus:.4f} -{exp_lim_minus:.4f}")
