'''
Created on Apr 23, 2020

@author: Tavis
'''
from root.nested.toa_data import get_data

event_key = "1920-OH-OSNQ"

team_oprs = {}
actual_score = {}
opr_score = {}
score_diff = {}

rankings_array = get_data("event/"+event_key+"/rankings").json()

for rankings in rankings_array:
    #print(rankings)
    #put the opr of each team into a dictionary
    team_oprs[rankings['team_key']] = rankings['opr']

#get all the matches
matches = get_data("event/"+event_key+"/matches").json()
#for each match in the event
for match in matches:
    #compare the expected score via opr and the actual score
    actual_score[match['match_key']+"-R"] = int(match['red_score'])
    actual_score[match['match_key']+"-B"] = int(match['blue_score'])
    #initialize the opr_score dictionary with all zeros
    opr_score[match['match_key']+"-R"] = 0
    opr_score[match['match_key']+"-B"] = 0
    
match_players = get_data("event/"+event_key+"/matches/participants").json()

for match_player in match_players:
    if match_player['station_status'] == 1:
        opr_score[match_player['match_participant_key'][:-1]]+=team_oprs[match_player['team_key']]
        
sum_diff = 0
red_score = blue_score = red_opr_score = blue_opr_score = 0
opr_correct = 0
for match in actual_score:
    score_diff[match] = actual_score[match]-opr_score[match]
    print(match[13:18]+match[-1:]+": "+str(round(score_diff[match], 1)))
    sum_diff+=abs(score_diff[match])
    
    if match[-1:] == "R":
        red_score = actual_score[match]
        red_opr_score = opr_score[match]
    else:
        blue_score = actual_score[match]
        blue_opr_score = opr_score[match]
        if (red_score > blue_score and red_opr_score > blue_opr_score) or (blue_score > red_score and blue_opr_score > red_opr_score):
            opr_correct+=1

#average amount that opr is off by
print(sum_diff/len(actual_score))
#percent of matches where winner is correctly predicted
print(opr_correct/len(actual_score))




