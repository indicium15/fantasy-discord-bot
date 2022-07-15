from nis import match
from xmlrpc.client import DateTime
from espn_api.basketball import League
import os.path
import json
import datetime
#Initialize League
league = League(league_id=916245033,year=2022,swid="{6446C104-AEF0-4C1E-9C83-74426FEE628E}",espn_s2="AEChDgJoQcjHLiG5vADjznN%2FCL6xWuhpeRl8zqsNLaQ67aAh3Er5SCnVT3kuSr4mvC92LgC7xqJeAYpfnw7TdIvSdBd%2Baf32zTuxm0CUjKn1LjtAGm%2Bf6SUkKXJt7Hf1sxsDxoaVPLSEoNjr4AgoRzQH7LVw45MMZn%2BeSXmDxvfy7810SA4qHEtH5v7OU3zDXH4jCM%2FEbUHUiHiYLa3f7alIZHIkcJ2Zt%2BmY95MZVkwIw2IU%2Fs88PAYltULzlr0XzfEHH3igNAlxUJR%2BqXiCO%2FMYpBrhmycgwQLjrTypVWERAA%3D%3D")
#rostered_players = []
# def set_league_id(league_id):
#     global league
#     league = League(league_id=league_id, year = DateTime)

def get_team_number():
    return len(league.teams)

def print_teams():
    answer = "Teams in League:\n"
    counter = 1
    for team in league.teams:
        answer += str(counter) + '. ' + team.team_name + ' (' + str(team.wins) + '-' + str(team.losses) + ')' '\n'
        counter += 1
    print(answer)
    return answer
        
def free_agents(size, position):
    answer = "Free Agents " + "(" + position + ")" + "\n"
    ret = league.free_agents(size=size, position=position)
    for re in ret:
        answer += re.name + '\n'
        answer += "Total Points: " + str(re.total_points) + '\n'
        answer += "Average Points: " + str(re.avg_points) + '\n'
        answer += "Projected Total Points: " + str(re.projected_total_points) + '\n'
        answer += "Projected Average Points: " + str(re.projected_avg_points) + '\n' + '\n'
    print(answer)
    return answer

def matchup():
    answer = ""
    matchups = league.scoreboard()
    for matchup in matchups:
        answer += matchup.home_team.team_name + " (" + str(matchup.home_team_live_score) + ")" + ' vs ' + str(matchup.away_team.team_name) + " (" + str(matchup.away_team_live_score) + ")" + '\n'
    print(answer)
    return answer

def activity():
    answer = "Recent Activity in the League\n"
    activities = league.recent_activity(size=6)
    for i, act in enumerate(activities):
        time = act.date / 1000.0
        answer += str(i+1) + ". "
        answer += str(datetime.datetime.fromtimestamp(time).strftime("%d-%m,%H:%M")) + '\n'
        answer += "**" + act.actions[0][0].team_name + "** " 
        answer += str.lower(act.actions[0][1]).replace("fa ", "") + " "
        answer += "**" + act.actions[0][2] + "**" '\n\n'
    print(answer)
    return answer

def player_lookup(name):
    rostered_players = []
    answer = ""
    for team in league.teams:
        for player in team.roster:
            print(player.points_breakdown)
            if(player.name == name):
                print(player.points_breakdown)
    #player = league.player_info(name=name)
    #print(player)
    pass
    
def team_info(team_number):
    answer = ""
    team = league.teams[team_number-1]
    answer += "Team Info for " + team.team_name + ": \n"
    answer += "Record: {}-{}\n".format(team.wins, team.losses)
    #TODO: Current Matchup
    #answer += "Current Matchup:\n"
    #current_match = team.schedule[-1]
    #print(current_match)
    #answer += "{} () vs {} ()".format(current_match)
    answer += "Roster: \n"
    for i, player in enumerate(team.roster): 
        answer += str(i+1) + ". " + player.name + "\n"
    print(answer)
    return answer

def current_box_scores():
    #matchup period = week number
    #scoring period = day number
    #league scoring = category, need to pass both to get box score
    scores = league.box_scores()
    for score in scores:
        print(score)

def waivers():
    answer = ""
    activity = league.recent_activity(msg_type="WAIVER")
    if(len(activity) == 0):
        answer = "No new waivers to report as of today."
    else:
        for act in activity:
            answer += str(act.date) + ": " + act.actions 
    
#Function Testing    
#print_teams()
#print(get_team_number())
#team_info(1)
#free_agents(5, "PF")
#matchup()
#activity()
#player_lookup("Lonzo Ball")
#current_box_scores()