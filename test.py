#statisitcs script for connect four game
import gamelogic as gl
import gamelogicfunctions as glf

fileText= ""
fileName= "output"
startIndexI= 0
startIndexJ= 0

def battle(playerMode1, playerMode2):
    global fileText, trainPlies
    fileText+= "************** " + playerMode1 + " VS. " + playerMode2 + " ************************\n"
    print fileText
    times= 2
    final= dict()
    final[playerMode1]= 0
    final[playerMode2]= 0
    for r in range(0,times):
        temp= playerMode1
        playerMode1= playerMode2
        playerMode2= temp
        wins= dict()
        wins[1.0]= 0
        wins[2.0]= 0
        wins[0.0]= 0
        numGames= 5
        for i in range (0, numGames):
            winner= gl.gamePlay(playerMode1, playerMode2, trainPlies, 0)
            wins[winner]+=1
        final[playerMode1]+=  wins[1]
        final[playerMode2]+= wins[2]    
        fileText+= "With " + playerMode1 + "=1 and " + playerMode2 + "=2, wins: " + str(wins) + "\n"
        #time.sleep(3)
    fileText+= "Final Results:\n"
    fileText+= str(final) +"\n"
    fileText+= "--------------------------------------------------------------\n"
    
def autotest():
    global fileText, fileName, startIndexI, startIndexJ
    players= ["Random","RandomPlus","RandomPlus2","RandomPlusPlus",\
              "BestLocalPlus","lookAheadOne","lookAheadTwice",\
              "lookAheadThrice","lookAheadOnePlus","lookAheadTwicePlus","lookAheadThricePlus",\
              "randomOffense","randomOffenseWithTwicePlus","randomOffenseOneWithTwicePlus",\
              "knnPlayer","minimaxKnn", "minimaxSeqCellsPlus"]
    for i in range(startIndexI, len(players)):
        for j in range(startIndexJ, len(players)):
            battle( players[i], players[j] )
            with open(fileName, 'a') as f:
                f.write( fileText )
            fileText= ""
        startIndexJ= i + 1        
    
trainPlies= dict()
trainPlies[1]= glf.getData()
trainPlies[2]= glf.adjustData(trainPlies[1], 2)
autotest()