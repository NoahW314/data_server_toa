'''
Created on Jul 28, 2019

@author: Tavis
'''
import requests
from root.nested.match_detail import get_velocity_vortex_details, get_relic_recovery_details, get_rover_ruckus_details

def get_data(url, params={}):
    return requests.get("https://theorangealliance.org/api/"+url, headers={"Content-Type":"application/json", 
                                                                    "X-TOA-Key":"9423996b25e096f32d99b965f138bd4a35435a7aa675d65ca54ff2112361eba7",
                                                                    "X-Application-Origin":"FTC Data Analysis"}, params=params)

'''SEASON DATA'''

def get_current_season():
    r = get_data("seasons")
    data = r.json()
    current_season = data[-1]
    return str(current_season["season_key"])
def get_prev_season_key(season_key):
    season_num1 = int(season_key[:2])
    
    if season_num1 == 10: return "0910"
    elif season_num1 < 10: return "0"+str(season_num1-1)+"0"+str(season_num1)
    else: return str(season_num1-1)+str(season_num1)
def get_prev_season_key_int(start_season):
    if len(str(start_season)) == 4:
        prev_season_key = str(start_season-1)[2:]+str(start_season)[2:]
    elif start_season == 10: prev_season_key = "0910"
    elif len(str(start_season)) == 2: 
        prev_season_key = str(start_season-1)+str(start_season)
    else:
        prev_season_key = "0"+str(start_season-1)+"0"+str(start_season)
    
    return prev_season_key
def check_season_key(key): 
    return key == "0506" or key == "0607"


def get_total_teams(season_key, current_season):
    if check_season_key(season_key):
        return None
    
    if season_key == current_season:
        r = get_data("team/", {"last_active":season_key})
    else:
        r = get_data("team/history/"+season_key)
    data = r.json()
    total_teams = len(data)
    return total_teams
def get_retired_teams(season_key, is_prev=True):
    if not is_prev:
        season_key = get_prev_season_key(season_key)
        
    if check_season_key(season_key):
        return None
        
    r = get_data("team/", {"last_active":season_key})
    data = r.json()
    retired_teams = len(data)
    return retired_teams


def get_total_events(season_key, type_=None):
    if type_ is None:
        r = get_data("event/", {"season_key":season_key})
    else: 
        r = get_data("event/", {"season_key":season_key, "type":type_})
        
    data = r.json()
    total_events = len(data)
    return total_events

def get_all_matches(season_key):
    matches, new_matches = [], []
    start = 0
    
    while True:
        r = get_data("match/all/"+season_key, {"start":start})
        if r.status_code != 200:
            break
        
        new_matches = r.json()
        start+=len(new_matches)
        matches.extend(new_matches)
        assert len(matches) == start
    
    return matches

def get_total_matches(season_key):
    start = 0
    
    while True:
        r = get_data("match/all/"+season_key, {"start":start})
        if r.status_code != 200:
            break
        start+=len(r.json())
    
    return start

def match_type_matches(match, type_):
    m_type = int(str(match["tournament_level"])[0])
    return type_ == m_type or (type_ == 5 and m_type >= 2 and m_type <= 4)

def get_details(season_key):
    return {"1819": get_rover_ruckus_details(),
            "1718": get_relic_recovery_details(),
            "1617": get_velocity_vortex_details(),    
            }[season_key]
def get_matches_detail_info(matches, season_key):
    details = get_details(season_key)
    return get_matches_info(matches, details, use_max=False)

def get_all_matches_score_info(season_key, type_=None):
    """type_ should follow the TOA match type guidelines (0-4)
    no distinction is made between semi/quarter final series
    a 5 will indicate any elimination match.
    """
    
    matches = get_all_matches(season_key)
    
    if type_ is not None: matches = [match for match in matches if match_type_matches(match, type_)]
        
    return get_matches_score_info(matches)
    
def get_matches_score_info(matches, use_ave=True, use_max=True):
    scores = ["red_score", "blue_score", "red_auto_score", "blue_auto_score", "red_tele_score", "blue_tele_score", 
              "red_end_score", "blue_end_score", "red_penalty", "blue_penalty"]
    return get_matches_info(matches, scores, use_ave, use_max)

def get_matches_info(matches, props, use_ave=True, use_max=True):
    num_matches = len(matches)
    totals = {"skipped":0}
    maxes = {}
    info = {}
    
    for s in props:
        if use_ave:
            totals["total_"+s] = 0
        if use_max and "red_" in s:
            maxes["highest_"+s.replace("red_", "")] = 0
    for match in matches:
        infos = calc_total(props, match, totals, maxes, calc_tots=use_ave, calc_max=use_max)
        totals = infos[0]
        maxes = infos[1]
        
    if use_ave:
        info = calc_ave(props, totals, num_matches-totals["skipped"])
    if use_max:
        info.update(maxes)
    
    return info


def calc_total(keys, match, tots, maxes, calc_tots=True, calc_max=True):
    for k in keys:
        if match[k] is None and calc_tots:
            tots["skipped"]+=1
        else: 
            score = match[k]
            if calc_tots:
                tots["total_"+k]+=score
            if calc_max and "red_" in k and score > maxes["highest_"+k.replace("red_", "")]:                    
                maxes["highest_"+k.replace("red_", "")] = score
                if k == "red_end_score" and score > 100:
                    maxes["highest_end_score"] = 100
    return (tots, maxes)
def calc_ave(keys, tots, num):
    ave_obj = {}
    for k in keys:
        if num == 0: ave_obj["average_"+k] = None
        else: ave_obj["average_"+k] = tots["total_"+k]/num
    for k in keys[::2]:
        key = k.replace("red_", "")
        if ave_obj["average_"+k] is None or ave_obj["average_blue_"+key] is None:
            ave_obj["average_"+key] = None
        else:
            ave_obj["average_"+key] = (ave_obj["average_"+k]+ave_obj["average_blue_"+key])/2
    return ave_obj
