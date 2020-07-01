players={'Drew':1450,'JZ':900,'Mike':950,'Alo':650,'Arno':800,'Will':750,'Jind':550,'Wang':400,'JsnH':600,'Gun':700,'Danl':750} #scores of players
teamNum=2 #number of teams we want in the game
GamingPlayers=['Alo','Will','Wang','JZ','Mike','Drew']# players who will be in the match

import random

def indOfWeakest(Teams):
    indW=0
    weakestSum=TeamSum(Teams[0])
    for ind in range(len(Teams)):
        if weakestSum>TeamSum(Teams[ind]):
            indW=ind
            weakestSum=TeamSum(Teams[ind])
    return indW

def randomPartition(numbers,n):
    Teams=[]
    for team in range(n):
        Teams+=[[]]
    for number in numbers:
        Teams[random.randrange(n)]+=[number]
    return sorted(Teams)

def evenishPartition(numbers,n):
    random.shuffle(numbers)
    Teams=[]
    #playerSum=TeamSum(numbers)
    for team in range(n):
        Teams+=[[]]
    weakestInd=indOfWeakest(Teams)
    for number in numbers:
        Teams[weakestInd]+=[number]
        weakestInd=indOfWeakest(Teams)
    i=0
    for Team in Teams:
        #print(Team,' now becomes...')
        Teams[i]=sorted(Team)
        #print('   ',Teams[i])
        #print(Teams)
        i+=1
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


def BestTeams(players1,setupNum,teamNum,gamble):
    players1=sorted(players1)
    maxNameLength=0
    for player in players1:
        maxNameLength=max(maxNameLength,len(player))
    PossibleTeams=[]
    worst=[players1]+[[]]*(teamNum-1)
    for team in range(setupNum):
        PossibleTeams+=[worst]
    for ind in range(2000):
        #partition=randomPartition(players1,teamNum)
        partition=evenishPartition(players1,teamNum)
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
        returns=Returns(teams,gamble)
        printouts=[]
        for team in teams:
            printout=''
            for player in team:
                bit1=1+maxNameLength-len(player)
                score=str(players[player])
                bit2=4-len(score)
                printout+=bit1*' '+player+':'+score+bit2*' '+' '
            printouts+=[printout]
        Len=0
        for printout in printouts:
            Len=max(Len,len(printout))
        ind=0
        for team in teams:
            printout=printouts[ind]
            print(printout+' '*(Len-len(printout))+'  total=',TeamSum(team),' loss:',returns[ind][0],' gain:',returns[ind][1])
            ind+=1
        print(' '*Len,'advantage=',PartitionInequality(teams))
    return(PossibleTeams)

def Returns(teams,gamble):
    teamTotals=[]
    for team in teams:
        teamTotals+=[TeamSum(team)]
    returns=[]
    ind=0
    for team in teams:
        returns+=[[round(-1*gamble),round(gamble*((sum(teamTotals)-teamTotals[ind])/teamTotals[ind]))]]
        ind+=1
    return returns

def scoreUpdate(teams,gamble,winnerInd):
    returns=Returns(teams,gamble)
    for player in players:
        for ind in range(len(teams)):
            team=teams[ind]
            if player in team:
                if ind==winnerInd:
                    players[player]+=returns[ind][1]
                if ind!=winnerInd:
                    players[player]+=returns[ind][0]
    print(players)
    

matches=BestTeams(GamingPlayers,5,teamNum,50)
#evenishPartition(GamingPlayers,2)
