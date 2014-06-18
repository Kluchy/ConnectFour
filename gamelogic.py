#Game Logic
#matplotlib grid inverses columns and rows, so matrxi[y,x] is actually grid[x,y]
import gui
import gamelogicfunctions as glf
import aiplayer as ai
import matplotlib.pyplot as plt
import numpy as py
import math


'''def startGame():
    boardHandler= gui.createBoard()
    shape= (gui.NUM_ROWS, gui.NUM_COLUMNS)
    gameBoard= py.zeros(shape)
            
def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)
    return event.button, event.x, event.y

def getPlayerMove(boardHandler):
    cid = boardHandler.canvas.mpl_connect('button_press_event', onclick)'''

'''Main function: starts a game between player1Mode and player2Mode
  '@param player1Mode, player2Mode - the players for the game
  '@param  useGui - flag to display gui
  '@calling gui.createBoard,gui.NUM_ROWS, gui.NUM_COLUMNS, gui.PLAYER1_COLOR,
             gui.PLAYER2_COLOR, glf.playMove, glf.isMoveValid, ai.randomMove,
             ai.randomMovePlus, ai.randomMovePlus2, glf.moveYieldsWin, glf.gameContainsTie
  '''
def gamePlay(player1Mode, player2Mode, useGui=1):
    sequentialPositionsNeeded= 4
    playerModes= {1:player1Mode, 2:player2Mode}
    if useGui:
        plt.ion()
        boardHandler= gui.createBoard()
        
    shape= (gui.NUM_ROWS, gui.NUM_COLUMNS)
    gameBoard= py.zeros(shape)
    winner= -1
    playerTurn= 1
    playerColor= gui.PLAYER1_COLOR
    while winner == -1:
        moveValid= True
        print "-------------------------------------------------Start Turn---------------------------------------------"
        print playerTurn
        if playerModes[playerTurn] == "Human":
            res= boardHandler.ginput(n=1, timeout=9999999)
            #print "receiving input: "
            #print res
            x,y= res[0] 
            x,y= math.floor(x),math.floor(y)
            #print "Clicked cell " + str(x) + "-" + str(y)
            #update gameBoard if move valid
            if glf.isMoveValid( x, gameBoard ):
                matrixX,matrixY= glf.playMove( (x,y), gameBoard, boardHandler, playerColor, playerTurn )
                #print gameBoard
                #print "matrixX: " + str(matrixX)
                #print "matrixY: " + str(matrixY)
            else:
                #request click from same player
                moveValid= False
                print "move not valid. please click in a cell"
        elif playerModes[playerTurn] == "Random":
                matrixX,matrixY= ai.randomMove(gameBoard)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "RandomPlus":
                matrixX,matrixY= ai.randomMovePlus(gameBoard)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "RandomPlus2":
                matrixX,matrixY= ai.randomMovePlus2(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "RandomPlusPlus":
                matrixX,matrixY,isRandom= ai.randomMovePlusPlus(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "BestLocal":
                matrixX,matrixY= ai.bestLocalMove(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "BestLocalPlus":
                (matrixX,matrixY),isBlockOrWin= ai.bestLocalMovePlus(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "lookAheadOne":
                (matrixX,matrixY),isBlockOrwin= ai.lookAheadOne(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "lookAheadTwice":
                (matrixX,matrixY),isBlockOrWin= ai.lookAheadTwice(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "lookAheadThrice":
                (matrixX,matrixY),isBlockOrWin= ai.lookAheadThrice(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "lookAheadOnePlus":
                (matrixX,matrixY),isBlockOrwin= ai.lookAheadOnePlus(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "lookAheadTwicePlus":
                (matrixX,matrixY),isBlockOrwin= ai.lookAheadTwicePlus(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "lookAheadThricePlus":
                (matrixX,matrixY),isBlockOrwin= ai.lookAheadThricePlus(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "randomOffense":
                (matrixX,matrixY),isBlockOrwin= ai.randomOffense(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        elif playerModes[playerTurn] == "randomOffenseWithTwicePlus":
                (matrixX,matrixY),isBlockOrwin= ai.randomOffenseWithTwicePlus(gameBoard, playerTurn)
                matrixX,matrixY= glf.playMove( (matrixY,matrixX), gameBoard, boardHandler, playerColor, playerTurn )
        print "-------------------------------------------------End Turn---------------------------------------------"
        if moveValid:
            res,winner,pos= glf.moveYieldsWin( gameBoard, sequentialPositionsNeeded, (matrixX,matrixY), playerColor )
            if res:
                print "WE HAVE A WINNER!!"
                print winner
                print "positons are: "
                print pos
                return winner
            elif glf.gameContainsTie(gameBoard):
                print "Game is Tied!! GG"
                return 0
            #next player's turn
            if playerTurn == 1:
                playerTurn= 2
                playerColor= gui.PLAYER2_COLOR
            else:
                playerTurn= 1
                playerColor= gui.PLAYER1_COLOR
        

gamePlay("Human","randomOffenseWithTwicePlus",1)
#gamePlay("lookAheadTwicePlus","lookAheadOnePlus",1)
'''testing yieldsWin
b= py.zeros((6,7))
b[0,0:3]= 1
b[1:4,0]= 2
b[4,0]= 2
b[0,4]= 1
b[1,1]= 1
b[2,2]= 1
b[3,3]= 2
res,winner,pos= moveYieldsWin(b, 4, (3,0),'r')'''