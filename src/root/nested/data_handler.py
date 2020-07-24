'''
Created on Jul 22, 2019

@author: Tavis
'''
from root.nested import toa_data as toa
from root.nested.util import set_if_none, event_types
from root.nested.toa_data import get_current_season

def process_data(data):
    return {
        "team": process_team(data),
        "match": process_match(data),
        "event": process_event(data),
        "region": process_region(data),
        "season": process_season(data)
    }.get(data["AnalysisType"], "<br><br>Result HTML")
def process_team(data):
    return "<br><br>Team "+data["InfoType"]+" "+data["SecondaryAnalysisType"]
def process_match(data):
    return "<br><br>Match "+data["InfoType"]+" "+data["SecondaryAnalysisType"]
def process_event(data):
    return "<br><br>Event "+data["InfoType"]+" "+data["SecondaryAnalysisType"]
def process_region(data):
    return "<br><br>Region "+data["InfoType"]+" "+data["SecondaryAnalysisType"]
def process_season(data):
    #"<br><br>Season "+data["InfoType"]+" "+data["SecondaryAnalysisType"]
    return_html = ""
    if data["InfoType"] == "info":
        start_season = int(data["InputData"]["name"])
        season_key = str(start_season)[2:]+str(start_season+1)[2:]
        prev_season_key = str(start_season-1)[2:]+str(start_season)[2:]
        current_season = get_current_season()
        
        team_info = get_season_team_info(season_key, prev_season_key, current_season)
        event_info = get_season_event_info(season_key)
        match_info = get_season_match_info(season_key)
        
        return_html = "<br><br>"+team_info+"<br><br>"+event_info+"<br><br>"+match_info
        
                
    return return_html

def get_season_team_info(season_key, prev_season_key, current_season):
    if season_key == "0506" or season_key == "0607":
        return "No Team Data is available for the 20"+season_key[:2]+"-20"+season_key[2:]+" season"
    
    total_teams = set_if_none(0, toa.get_total_teams, season_key, current_season)
    prev_total_teams = set_if_none(0, toa.get_total_teams, prev_season_key, current_season)
    retired_teams = set_if_none(0, toa.get_retired_teams, season_key, False)
    
    return ("Total Teams: "+str(total_teams)+"&emsp;More than last season: "+str(total_teams-prev_total_teams)+
            "<br>Teams Retired Last Season: "+str(retired_teams)+"&emsp;Teams Added: "+str(total_teams-prev_total_teams+retired_teams))
def get_season_event_info(season_key):
    total_events = set_if_none(0, toa.get_total_events, season_key)
    events_per_type = {}
    event_type_string = ""
    i = 0
    for t in event_types:
        i = i+1
        events_per_type[t] = set_if_none(0, toa.get_total_events, season_key, _type=t)
        if i%2 == 1: event_type_string+="&emsp;"
        else: event_type_string+="<br>"
        event_type_string+=event_types[t]+": "+str(events_per_type[t])
        
    return ("Total Events: "+str(total_events)+event_type_string)
def get_season_match_info(season_key):
    
    return ("Total Matches: ")



