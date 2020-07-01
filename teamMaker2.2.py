import itertools

ELOS = {'Drew':1450, 'JZ':900, 'Mike':950, 'Alo':650, 'Arno':800, 'Will':750, 'Jind':550, 'Wang':400}  # scores of players

def team_score(players):
    return sum(ELOS[p] for p in players)

def print_team(team_index, team):
    print("  Team {} ({}):".format(team_index, team_score(team)))
    for p in team:
        print("    {} ({})".format(p, ELOS[p]))

def show_best_teams(players, num_teams=2, results_to_show=3):
    results = set()  # (team_score_difference, team_1, team_2)
    for order in itertools.permutations(players):
        # Choose teams by deciding positions at which to split the permutation
        for inds in itertools.combinations(range(len(players)), num_teams-1):
            inds = (0,) + inds + (len(players),)
            teams = [ order[inds[i]:inds[i+1]] for i in range(num_teams) ]
            scores = [ team_score(team) for team in teams ]
            mean = sum(scores) / len(scores)
            unfairness = sum(abs(score-mean) for score in scores)
            # Use a set to deduplicate equivalent teams.
            # Using frozenset instead of set because frozenset, unlike set, is hashable
            results.add((unfairness, frozenset(frozenset(team) for team in teams)))
    for diff, teams in sorted(results)[:results_to_show]:
        returns=Returns(teams,gamble=50) #calculates the loss and gain for a team
        print("----- Result with unfairness {} -----".format(diff))
        for i, team in enumerate(teams):
            print_team(i+1, team)
            print('  loss:',returns[i][0],'  gain:',returns[i][1]) # prints the loss and gain
    return sorted(results)[:results_to_show]
#####
def Returns(teams,gamble=50): #calculates the losses and gain of each team
    teamTotals=[]
    for team in teams:
        teamTotals+=[team_score(team)]
    #print(teamTotals)
    returns=[]
    ind=0
    for team in teams:
        returns+=[[round(-1*gamble),round(gamble*((sum(teamTotals)-teamTotals[ind])/teamTotals[ind]))]]
        #print(((sum(teamTotals)-teamTotals[ind])/teamTotals[ind]))
        ind+=1
    #print(returns)
    return returns

def score_update(teams,winnerInd,gamble=50): #updates ELOS depending on the victors of a given match
    returns=Returns(teams,gamble)
    for player in ELOS:
        for ind in range(len(teams)):
            team=teams[ind]
            if player in team:
                if ind==winnerInd:
                    ELOS[player]+=returns[ind][1]
                if ind!=winnerInd:
                    ELOS[player]=max(20,ELOS[player]+returns[ind][0])
    print(ELOS)
###

num_teams = 3
gaming_players = ['Alo', 'Will', 'Wang', 'JZ', 'Mike', 'Drew'] 
matches=show_best_teams(gaming_players, num_teams=num_teams)
#print(matches)
print('if the first match is played and Team 2 wins, the ELOS is updated as below')
score_update(list(matches[0][1]),1)
