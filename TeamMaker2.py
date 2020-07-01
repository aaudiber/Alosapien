import itertools

ELOS = {'Drew':145, 'JZ':90, 'Mike':95, 'Alo':65, 'Arno':80, 'Will':75, 'Jind':55, 'Wang':40}  # scores of players

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
        print("----- Result with unfairness {} -----".format(diff))
        for i, team in enumerate(teams):
            print_team(i+1, team)

num_teams = 2
gaming_players = ['Alo', 'Will', 'Wang', 'JZ', 'Mike', 'Drew'] 
show_best_teams(gaming_players, num_teams=num_teams)
