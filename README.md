# PyHF simple template tools

Collection of templates for common stat operations


# Simplified x-section upper limits DV+Jets

Using `model-agnostic-dvjets.py`.

## High-pT SR
Signal: 1.36 (0.01fb arbitrary x-section)
Background: 0.46+0.27-0.30
Data: 1

Toy-based, 1k toys:  mu_exp = 2.3407 +0.8592 -0.1032,  mu_obs = 2.9363
Toy-based, 10k toys: mu_exp = 2.2179 +0.7020 -0.0544,  mu_obs = 2.1809
Asymptotics:         mu_exp = 2.1658 +1.5050 -0.8356,  mu_obs = 2.7065

## Trackless SR
Signal: 1.36 (0.01fb arbitrary x-section)
Background: 0.83+0.51-0.53
Data: 0

Toy-based, 1k toys:  mu_exp = 2.1754 +0.9542 -0.0652,  mu_obs = 2.1616
Toy-based, 10k toys: mu_exp = 2.2160 +0.2840 -0.1160,  mu_obs = 2.2005
Asymptotics:         mu_exp = 2.1713 +1.4943 -0.8284,  mu_obs = 1.6432

