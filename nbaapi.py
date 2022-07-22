from requests import get
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playerprofilev2, playercareerstats, playerdashboardbyyearoveryear, commonplayerinfo, playerestimatedmetrics, teamestimatedmetrics, leaguehustlestatsplayerleaders, leagueleaders, leagueseasonmatchups, playerdashboardbyopponent
#https://github.com/swar/nba_api

def get_team_id(name):
    print(len(name))
    if(len(name) == 3):
        try:
            response = teams.find_team_by_abbreviation(name)
            print(response['id'], response['full_name'])
            return(response['id'])
        except:
            return -1 
    elif(" " in name):
        try:
            response = teams.find_teams_by_full_name(name)
            if(len(response) == 1):
                print(response[0]['id'], response[0]['full_name'])
                return(response[0]['id'])
            else: return -1
        except:
            return -1
    else:
        try:
            response = teams.find_teams_by_nickname(name)
            if(len(response) == 1):
                print(response[0]['id'], response[0]['full_name'])
                return(response[0]['id'])
            else:
                return -1
        except:
            return -1

def get_player_name(id):
    try:
        results = players.find_player_by_id(int(id))
        return results['full_name']
    except:
        print("Invalid player ID, please try again.")

def get_player_id(name):
    results = players.find_players_by_full_name(str(name))
    #print(results, len(results))
    if len(results) == 0:
        return("Sorry, we were unable to find the player you were looking for. Please try again.")
    elif len(results) == 1:
        player_id = results[0]['id']
        print(player_id)
        return player_id
    elif len(results) > 1:
        output = "Your query returned too many results. Were you looking for:\n"
        for player in results:
            output += player['full_name']
            print(output)
            return output

def season_stats_lookup(player_id, season='2021-22'):
    stats = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id=player_id, season=season, per_mode_detailed='PerGame')
    dictionary = stats.overall_player_dashboard.get_dict()
    print(dictionary)
    reply = "Stats for {} in {}\n".format(get_player_name(player_id),dictionary['data'][0][1])
    reply += "{:<9}".format('GP, MPG : ') + "{:^2}, ".format(dictionary['data'][0][5]) + "{:^2}".format(dictionary['data'][0][9]) + "\n\n"
    reply += '*Overview*:\n'
    reply += '{:<6}'.format('PTS : ') + '{:^4}'.format(dictionary['data'][0][29])+'\n'
    reply += '{:<6}'.format('AST : ') + '{:^4}'.format(dictionary['data'][0][22])+'\n'
    reply += '{:<6}'.format('REB : ') + '{:^4}'.format(dictionary['data'][0][21])+'\n'
    reply += '{:<6}'.format('TOV : ') + '{:^4}'.format(dictionary['data'][0][23])+'\n\n'
    reply += '*Shooting*:\n'
    reply += '{:<15}'.format('FG, FGA, FG% : ') + '{:^4},'.format(dictionary['data'][0][10]) + ' {:^4},'.format(dictionary['data'][0][11]) + ' {:^4.1%}'.format(dictionary['data'][0][12])+'\n'
    reply += '{:<15}'.format('3P, 3PA, 3P% : ') + '{:^4},'.format(dictionary['data'][0][13]) + ' {:^4},'.format(dictionary['data'][0][14]) + ' {:^4.1%}'.format(dictionary['data'][0][15])+'\n'
    reply += '{:<15}'.format('FT, FTA, FT% : ') + '{:^4},'.format(dictionary['data'][0][16]) + ' {:^4},'.format(dictionary['data'][0][17]) + ' {:^4.1%}'.format(dictionary['data'][0][18])+'\n\n'
    reply += '*Rebounding*:\n'
    reply += '{:<11}'.format('ORB, DRB : ') +  '{:^4},'.format(dictionary['data'][0][19]) + ' {:^4}'.format(dictionary['data'][0][20])+'\n\n'
    reply += '*Defensive*:\n'
    reply += '{:<15}'.format('STL, BLK, PF : ') + '{:^4},'.format(dictionary['data'][0][24]) + ' {:^4},'.format(dictionary['data'][0][25]) + ' {:^4}'.format(dictionary['data'][0][27])+'\n'     
    print(reply)
    return(reply)

def get_season_stats(name, season='2021-22'):
    try:
        player_id = get_player_id(name)
        response = season_stats_lookup(player_id, season)
        return response
    except Exception as e:
        return(str(e))

def estimated_metrics(player_name,season='2021-22'):
    player_id = get_player_id(player_name)
    try:
        response = playerestimatedmetrics.PlayerEstimatedMetrics(league_id='00',season=season,season_type='Regular Season').get_dict()['resultSet']['rowSet']
        #print(response)
        for player in response:
            #print(player)
            if player[0] == player_id:
                #print("Player Found")
                answer = "\nEstimates for {} (With Rankings):\n".format(player[1])
                answer += "{:12}".format("ORTG, DRTG: ") + "{:^4} (#{:^3}), ".format(player[6],player[-10]) + "{:^4} (#{:^3})\n".format(player[7],player[-9]) 
                #answer += "{:<12}{:^4} (#{:^3}), {:^4} (#{:^3})\n".format("ORTG, DRTG: ",player[6],player[-10],player[7],player[-9])
                answer += "{:<8}{:^4} (#{:^3})\n".format("NETRTG: ",player[8],player[-8])
                answer += "ASTRATIO: {} (#{})\n".format(player[10],player[-7])
                answer += "OREB%, DREB%: {:.1%} (#{}), {:.1%} (#{})\n".format(player[11],player[-6],player[12],player[-5])
                answer += "REB%: {:.1%} (#{})\n".format(player[13],player[-4])
                answer += "TOV%, USG%: {:.1%} (#{}), {:.1%} (#{})\n".format(player[14],player[-3],player[15],player[-2])
                answer += "PACE: {} (#{})\n".format(player[16],player[-1])
        print(answer)
        return answer
        # for player in (response['resultSet']['rowSet'][0]):
        #     print(player)
        #     if player[0] == player_id:
        #         print("Player Found")
        #if player[0] == player_id:
        #for player in response.values():
                #print("Player Found")
    except:
        return("An error has occured, please try again.")

def team_estimated_metrics(team_name,season="2021-22"):
    answer = ""
    team_id = get_team_id(team_name)
    if(team_id == -1):
        answer = "Error finding the team, please try again."
        return answer
    response = teamestimatedmetrics.TeamEstimatedMetrics(league_id='00', season=season, season_type="Regular Season").get_dict()['resultSet']['rowSet']
    for team in response:
        if team_id == team[1]:
            print(team[0])
            answer += "Estimated Stats for {}\n".format(team[0])
            answer += "Record: {}-{}\n".format(team[3],team[4])
            answer += "ORTG: {} (#{})\n".format(team[7],team[-9])
            answer += "DRTG: {} (#{})\n".format(team[8],team[-8])
            answer += "NETRTG: {} (#{})\n".format(team[9],team[-7])
            answer += "PACE: {} (#{})\n".format(team[10],team[-1])
            answer += "ASTRATIO: {} (#{})\n".format(team[12],team[-6])
            answer += "OREB%: {:.1%} (#{})\n".format(team[13],team[-5])
            answer += "DREB%: {:.1%} (#{})\n".format(team[14],team[-4])
            answer += "REB%: {:.1%} (#{})\n".format(team[15],team[-3])
            answer += "TOV%: {:.1%} (#{})\n".format(team[16],team[-2])
            print(answer)
            return(answer)

def hustle_stats_leaders(stat_choice, season='2021-22'):
    response = leaguehustlestatsplayerleaders.LeagueHustleStatsPlayerLeaders(per_mode_time="PerGame",season_type_all_star="Regular Season",season=season)
    if(stat_choice == 1):
        response = response.player_charges_drawn_leaders.get_dict()['data']
        print(response)
        answer = "Charges Drawn Per Game Leaders:\n"
        for player in response:
            answer += "{} - {} ({})\n".format(player[-2],player[1],player[-1])
        print(answer)
        return(answer)
    elif(stat_choice == 2):
        response = response.player_contested_shots_leaders.get_dict()['data']
        print(response)
        answer = "Contested Shots Per Game Leaders:\n"
        for player in response:
            answer += "{} - {} ({})\n".format(player[-2],player[1],player[-1])
        print(answer)
        return(answer)
    elif(stat_choice == 3):
        response = response.player_deflections_leaders.get_dict()['data']
        print(response)
        answer = "Deflected Shots Per Game Leaders:\n"
        for player in response:
            answer += "{} - {} ({})\n".format(player[-2],player[1],player[-1])
        print(answer)
        return(answer)
    elif(stat_choice == 4):
        response = response.player_loose_ball_leaders.get_dict()['data']
        print(response)
        answer = "Loose Balls Per Game Leaders:\n"
        for player in response:
            answer += "{} - {} ({})\n".format(player[-2],player[1],player[-1])
        print(answer)
        return(answer) 
    elif(stat_choice == 5):
        response = response.player_screen_assist_leaders.get_dict()['data']
        print(response)
        answer = "Screen Assists Per Game Leaders:\n"
        for player in response:
            answer += "{} - {} ({})\n".format(player[-2],player[1],player[-1])
        print(answer)
        return(answer)
    else:
        return("Invalid selection, please try again.")

def league_leaders(stat_choice, season="2021-22"):
    response = leagueleaders.LeagueLeaders(league_id="00",per_mode48="PerGame",scope="RS",season=season,season_type_all_star="Regular Season",stat_category_abbreviation=stat_choice)
    print(response.league_leaders.get_dict()['data'][:10])
    pass

def matchup_data(offensive_player, defensive_player):
    temp_offensive = offensive_player.strip()
    temp_defensive = defensive_player.strip()
    off_player_id = get_player_id(temp_offensive)
    def_player_id = get_player_id(temp_defensive)
    response = leagueseasonmatchups.LeagueSeasonMatchups(league_id="00",per_mode_simple="Totals",season="2021-22",season_type_playoffs="Regular Season", off_player_id_nullable=off_player_id, def_player_id_nullable=def_player_id).season_matchups.get_dict()['data'][0]
    #print(response)
    answer = "**Total Matchup Data:**\n"
    answer += "Offensive Player: {}\n".format(response[2])
    answer += "Defensive Player: {}\n".format(response[4])
    answer += "Matchup Minutes: {}\n".format(response[6])
    answer += "Partial Possessions: {}\n".format(response[7])
    answer += "Points: {}\n".format(response[9])
    answer += "Assists: {}\n".format(response[10])
    answer += "Turnovers: {}\n".format(response[11])
    answer += "Blocks: {}\n".format(response[12])
    answer += "FGM / FGA: {}/{} ({:.1%})\n".format(response[13],response[14],response[15])
    answer += "FG3M / FG3A / 3P%: {}/{} ({:.1%})\n".format(response[16],response[17], response[18])
    answer += "FTM / FTA: {}/{}".format(response[-3],response[-2])
    print(answer)
    return answer


#Function Testing
#matchup_data(" LeBron James "," Nikola Jokic ")
#league_leaders("PTS")
#hustle_stats_leaders(5)
#get_team_id("Bulls")
#print(teams.get_teams())
#team_estimated_metrics("Chicago Bulls")
#get_season_stats("Lonzo Ball")
#get_player_id("Evan Mobley")
#print(get_player_name(4432816))
#estimated_metrics(player_name="Lonzo Ball")