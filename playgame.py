import gamelogicfunctions as glf
import gamelogic as gl
'''Run this script to launch an instance of a Connect4 game against one of our AIs.
    For a human player, make one of the first two arguments "Human".
    To choose one of our numerous AIs, copy and paste one of these names as the
    second player argument (this list is ordered by increasing level of difficulty
    according to our automated and user testing mothods):
    . Random
    . RandomPlus
    . knnPlayer
    . minimaxKnn
    . RandomPlus2
    . RandomPlusPlus
    . LookAheadthrice
    . lookAheadOne
    . LookAheadOnePlus
    . lookAheadTwice
    . BestLocalPlus
    . randomOffenseOneWithTwicePlus
    . minimaxSeqCellsPlus
    . lookAheadThricePlus
    . randomOffense
    . LookAheadTwicePlus
    . randomOffenseWithTwicePlus
    '''
def startGame(player1,player2):
    trainPlies= dict()
    trainPlies[1]= glf.getData()
    trainPlies[2]= glf.adjustData(trainPlies[1], 2)
    gl.gamePlay(player1, player2,trainPlies)    

startGame("Human","randomOffenseWithTwicePlus")