#statisitcs script for connect four game
import gamelogic as gl
import aiplayer as ai
import time

def battle(playerMode1, playerMode2):
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
            winner= gl.gamePlay(playerMode1, playerMode2,1)
            wins[winner]+=1
        final[playerMode1]+=  wins[1]
        final[playerMode2]+= wins[2]    
        print "With ", playerMode1,"=1 and ", playerMode2,"=2, wins: ", wins
        #time.sleep(3)
    print final
battle("lookAheadTwicePlus", "lookAheadThrice")
#battle("lookAheadOnePlus", "lookAheadTwicePlus")