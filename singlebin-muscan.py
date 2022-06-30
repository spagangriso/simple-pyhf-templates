import pyhf
import numpy as np
import matplotlib.pyplot as plt
from pyhf.contrib.viz import brazil

pyhf.set_backend("numpy")

sig = {
    "name": "signal",
    "data": [6.0],
    "modifiers": [
        {
            "name": "mu",
            "type": "normfactor",
            "data": None
        }
    ]
}

bkg = {
    "name": "background",
    "data": [9.0],
    "modifiers": []   
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

print(f"========== MODEL =========================")
print(f"  aux data: {model.config.auxdata}")
#print(f"      down: {model.expected_data([-1.0])}")
#print(f"   nominal: {model.expected_data([0.0])}")
#print(f"        up: {model.expected_data([1.0])}")
print("")

poi_vals = np.linspace(0, 5, 41)
results = [
    pyhf.infer.hypotest(
        test_poi, data, model, test_stat="qtilde", return_expected_set=True,
#        calctype="toybased", ntoys=100
    )
    for test_poi in poi_vals
]

fig, ax = plt.subplots()
fig.set_size_inches(7, 5)
brazil.plot_results(poi_vals, results, ax=ax)
fig.show()

print("======== RESULTS =========")
for poi, cls_results in zip(poi_vals, results): #range(0,len(poi_vals))
    #results contain a list of (CLs_obs, (CLs_exp_m2sigma, CLs_exp_m1sigma, CLs_exp, CLs_exp_p1sigma, CLs_exp_p2sigma))
    cls_obs = cls_results[0]
    cls_exp = cls_results[1][2]
    cls_exp_plus = cls_results[1][3] - cls_exp
    cls_exp_minus = cls_exp - cls_results[1][1]
    print(f"mu = {poi}, CLs_obs = {cls_obs:.4f}, CLs_exp = {cls_exp:4f} +{cls_exp_plus:.4f} -{cls_exp_minus:.4f}")
    #    print(f"mu = {poi_vals[idx]}, CLs_obs = {cls_obs:.4f}, CLs_exp = {cls_exp:4f} +{cls_exp_plus:.4f} -{cls_exp_minus:.4f}")

