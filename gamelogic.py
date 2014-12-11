#Game Logic
#matplotlib grid inverses columns and rows, so matrxi[y,x] is actually grid[x,y]
import gui
import gamelogicfunctions as glf
import aiplayer as ai
import matplotlib.pyplot as plt
import numpy as py
import math
import time

'''Main function: starts a game between player1Mode and player2Mode
  '@param player1Mode, player2Mode - the players for the game
  '@param  useGui - flag to display gui
  '@calling gui.createBoard,gui.NUM_ROWS, gui.NUM_COLUMNS, gui.PLAYER1_COLOR,
             gui.PLAYER2_COLOR, glf.playMove, glf.isMoveValid, ai.randomMove,
             ai.randomMovePlus, ai.randomMovePlus2, glf.moveYieldsWin, glf.gameContainsTie,
             ai.RandomPlusPlus, ai.bestLocalMove, ai.lookAheadOne, ai.lookAheadTwice,
             ai.lookAheadThrice, ai.lookAheadOnePlus, ai.lookAheadTwicePlus,
             ai.lookAheadThricePlus, ai.randomOffense, ai.randomOffenseWithTwicePlus,
             ai.randomOffenseOneWithTwicePlus, ai.forwardEval, ai.knnPlayer,
             ai.minimaxKnn, ai.minimaxSeqCellsPlus
  '''
def gamePlay(player1Mode, player2Mode,trainPlies=None, useGui=1):
    sequentialPositionsNeeded= 4
    playerModes= {1:player1Mode, 2:player2Mode}
    if useGui:
        plt.ion()
        boardHandler= gui.createBoard()
    else:
        boardHandler= None
        
    shape= (gui.NUM_ROWS, gui.NUM_COLUMNS)
    gameBoard= py.zeros(shape)
    winner= -1
    playerTurn= 1
    playerColor= gui.PLAYER1_COLOR
    cumulatedTime= 0.0
    numMoves= 0
    while winner == -1:
        moveValid= True
        #print "-------------------------------------------------Start Turn---------------------------------------------"
        #print playerTurn
        if playerModes[playerTurn] == "Human":
            res= boardHandler.ginput(n=1, timeout=9999999)
            x,y= res[0] 
            x,y= math.floor(x),math.floor(y)
            #update gameBoard if move valid
            if glf.isMoveValid( x, gameBoard ):
                matrixX,matrixY= glf.playMove( (x,y), gameBoard, boardHandler, playerColor, playerTurn, useGui )
            else:
                #request click from same player
                moveValid= False
                print "move not valid. please click in a cell"
        elif playerModes[playerTurn] == "Random":
                startTime= time.time()
                matrixX,matrixY= ai.randomMove(gameBoard)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "RandomPlus":
                startTime= time.time()
                matrixX,matrixY= ai.randomMovePlus(gameBoard)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "RandomPlus2":
                startTime= time.time()
                matrixX,matrixY= ai.randomMovePlus2(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "RandomPlusPlus":
                startTime= time.time()
                (matrixX,matrixY),isRandom= ai.randomMovePlusPlus(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "BestLocal":
                startTime= time.time()
                matrixX,matrixY= ai.bestLocalMove(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "BestLocalPlus":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrWin= ai.bestLocalMovePlus(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "lookAheadOne":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.lookAheadOne(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "lookAheadTwice":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrWin= ai.lookAheadTwice(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "lookAheadThrice":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrWin= ai.lookAheadThrice(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "lookAheadOnePlus":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.lookAheadOnePlus(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "lookAheadTwicePlus":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.lookAheadTwicePlus(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "lookAheadThricePlus":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.lookAheadThricePlus(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "randomOffense":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.randomOffense(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "randomOffenseWithTwicePlus":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.randomOffenseWithTwicePlus(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "randomOffenseOneWithTwicePlus":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.randomOffenseOneWithTwicePlus(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "forwardEval":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.forwardEval(gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "knnPlayer":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.knnPlayer( trainPlies[playerTurn], gameBoard, playerTurn )
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "minimaxKnn":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.minimaxKnn( trainPlies[playerTurn], gameBoard, playerTurn)
                endTime= time.time()
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
        elif playerModes[playerTurn] == "minimaxSeqCellsPlus":
                startTime= time.time()
                (matrixX,matrixY),isBlockOrwin= ai.minimaxSeqCellsPlus( None, gameBoard, playerTurn)
                endTime= time.time()
                #if not glf.isMoveValid( matrixX, gameBoard ):
                #    print "minimaxSeqCellsPlus returns invalid move: ", matrixX, matrixY
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn, useGui )
                
        #print "-------------------------------------------------End Turn---------------------------------------------"
        if moveValid:
            if playerTurn == 2:
                cumulatedTime+= endTime-startTime
                numMoves+=1
            res,winner,pos= glf.moveYieldsWin( gameBoard, sequentialPositionsNeeded, (matrixX,matrixY), playerColor )
            if res:
                print "WE HAVE A WINNER!!"
                print winner
                print "positons are: "
                print pos
                fileText= "average time for " + str(playerModes[2]) + " = " + str( cumulatedTime / numMoves )
                with open( 'times', 'a' ) as f:
                    f.write( fileText + "\n" )
                return winner
            elif glf.gameContainsTie(gameBoard):
                print "Game is Tied!! GG"
                fileText= "average time for " + str(playerModes[2]) + " = " + str( cumulatedTime / numMoves )
                with open( 'times', 'a' ) as f:
                    f.write( fileText + "\n" )
                return 0
            #next player's turn
            if playerTurn == 1:
                playerTurn= 2
                playerColor= gui.PLAYER2_COLOR
            else:
                playerTurn= 1
                playerColor= gui.PLAYER1_COLOR