players={'Drew':145,'JZ':90,'Mike':95,'Alo':65,'Arno':80,'Will':75,'Jind':55,'Wang':40} #scores of players
teamNum=2 #number of teams we want in the game
GamingPlayers=['Alo','Will','Wang','JZ','Mike','Drew']# players who will be in the match

import random

def randomPartition(numbers,n):
    Teams=[]
    for team in range(n):
        Teams+=[[]]
    for number in numbers:
        Teams[random.randrange(n)]+=[number]
    return sorted(Teams)

def TeamSum(Team):
    Sum=0
    for player in Team:
        Sum+=players[player]
    return Sum

def PartitionInequality(Teams):
    inequality=0
    for teamA in Teams:
        for teamB in Teams:
            inequality=max(inequality,TeamSum(teamA)-TeamSum(teamB))
    return inequality


def BestTeams(players1,setupNum,teamNum):
    players1=sorted(players1)
    maxNameLength=0
    for player in players1:
        maxNameLength=max(maxNameLength,len(player))
    PossibleTeams=[]
    worst=[players1]+[[]]*(teamNum-1)
    for team in range(setupNum):
        PossibleTeams+=[worst]
    for ind in range(2000):
        partition=randomPartition(players1,teamNum)
        value=PartitionInequality(partition)
        i=0
        while (partition not in PossibleTeams) and (i>-1*len(PossibleTeams)) and (value<PartitionInequality(PossibleTeams[i-1])):
            i-=1
        if i!=0:
            #print('ho ho, better yet ',i)
            #print('    ', partition,',',PartitionInequality(partition))
            #for teams in PossibleTeams:
            #    print(teams)
            #    print('     ',PartitionInequality(teams))
            #print('    ',PossibleTeams)
            PossibleTeams=PossibleTeams[:i]+[partition]+PossibleTeams[i:-1]
            #print('    ',PossibleTeams)
    print('Most even team setups found')
    for teams in PossibleTeams:
        printouts=[]
        for team in teams:
            printout=''
            for player in team:
                bit1=1+maxNameLength-len(player)
                score=str(players[player])
                bit2=3-len(score)
                printout+=bit1*' '+player+':'+score+bit2*' '+' '
            printouts+=[printout]
        Len=0
        for printout in printouts:
            Len=max(Len,len(printout))
        ind=0
        for team in teams:
            printout=printouts[ind]
            print(printout+' '*(Len-len(printout))+'  total=',TeamSum(team))
            ind+=1
        print(' '*Len,'advantage=',PartitionInequality(teams))

BestTeams(GamingPlayers,5,teamNum)
