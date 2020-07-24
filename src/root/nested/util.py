'''
Created on Jul 28, 2019

@author: Tavis
'''
from _collections import OrderedDict

def set_if_none(default, func, *args, **kwargs):
    var = func(*args, **kwargs)
    if var is None: var = default
    return var

event_types = OrderedDict({
    "LGCMP":"League Championship",
    "LGMEET":"League Meet",
    "OFFSSN":"Off Season",
    "QUAL":"Qualifier",
    "RCMP":"Region Championship",
    "SCRIMMAG":"Scrimmage",
    "SPRING":"Spring Event",
    "SPRQUAL":"Super Qualifier",
    "SPRRGNL":"Super Regional",
    "WRLDCMP":"World Championship",    
    "OTHER":"Other"
})