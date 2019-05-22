"""Rttov interface

Must be copied into the port/interface directory for each atmospheric plugin
and then updated.
"""

# Paths
DATA_DIR = 'data'
PROFILE_DIR = 'profiles'

# Keys
keys = [
        'downwell',
        'upwell',
        'tau',
        'wavenums',
    ]

# Updates
"""Updates must be made per-plugin."""
def get_downwell(rttov_obj):
    return rttov_obj.Rad2Down[0,:,-1]
def get_upwell(rttov_obj):
    return rttov_obj.Rad2Up[0,:,-1]
def get_tau(rttov_obj):
    return rttov_obj.TauTotal[0]
def get_wnums(rttov_obj):
    return rttov_obj.WaveNumbers
get_fromKey = {
        keys[0]: get_downwell,
        keys[1]: get_upwell,
        keys[2]: get_tau,
        keys[3]: get_wnums,
    }
