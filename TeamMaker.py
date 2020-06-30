PLAYERS = {'Drew':145,'JZ':90,'Mike':95,'Alo':65,'Arno':80,'Will':75,'Jind':55,'Wang':40} #scores of players
TEAM_NUM = 2 #number of teams we want in the game
GAMING_PLAYERS = ['Alo','Will','Wang','JZ','Mike','Drew']# players who will be in the match

import random

def random_partition(numbers,n):
    teams = []
    for team in range(n):
        teams += [[]]
    for number in numbers:
        teams[random.randrange(n)] += [number]
    return sorted(teams)

def team_sum(team):
    total=0
    for player in team:
        total += PLAYERS[player]
    return total

def partition_inequality(teams):
    inequality = 0
    for team_a in teams:
        for team_b in teams:
            inequality = max(inequality, team_sum(team_a) - team_sum(team_b))
    return inequality


def best_teams(players_1, setup_num, team_num):
    players_1 = sorted(players_1)
    max_name_length = 0
    for player in players_1:
        max_name_length = max(max_name_length, len(player))
    possible_teams = []
    worst = [players_1] + [[]]*(team_num-1)
    for team in range(setup_num):
        possible_teams += [worst]
    for ind in range(2000):
        partition = random_partition(players_1, team_num)
        value = partition_inequality(partition)
        i = 0
        while (partition not in possible_teams) and (i > -1*len(possible_teams)) and (value < partition_inequality(possible_teams[i-1])):
            i -= 1
        if i != 0:
            #print('ho ho, better yet ',i)
            #print('    ', partition,',',PartitionInequality(partition))
            #for teams in PossibleTeams:
            #    print(teams)
            #    print('     ',PartitionInequality(teams))
            #print('    ',PossibleTeams)
            possible_teams = possible_teams[:i] + [partition] + possible_teams[i:-1]
            #print('    ',PossibleTeams)
    print('Most even team setups found')
    for teams in possible_teams:
        printouts = []
        for team in teams:
            printout = ''
            for player in team:
                bit_1 = 1 + max_name_length - len(player)
                score = str(PLAYERS[player])
                bit_2 = 3 - len(score)
                printout += bit_1*' ' + player + ':' + score + bit_2*' ' + ' '
            printouts += [printout]
        max_len = 0
        for printout in printouts:
            max_len = max(max_len, len(printout))
        ind = 0
        for team in teams:
            printout = printouts[ind]
            print(printout + ' '*(max_len-len(printout)) + '  total=', team_sum(team))
            ind += 1
        print(' '*max_len, 'advantage=', partition_inequality(teams))

best_teams(GAMING_PLAYERS, 5, TEAM_NUM)
