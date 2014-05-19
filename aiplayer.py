#AI Players
import numpy as py
import random
import gamelogicfunctions as glf
import aifunctions as aif

'''random player: picks a random slot every time
   also use as default for smarter players
  '@param gameBoard - underlying matrix representing game grid
  '@return coordinates of cell in which player decides to play
  '''
def randomMove(gameBoard):
    numrows, numcolumns= py.shape(gameBoard)
    randomRow= random.randint(0,numrows-1)
    randomColumn= random.randint(0,numcolumns-1)
    while not glf.isMoveValid( randomColumn, gameBoard):
        randomRow= random.randint(0,numrows-1)
        randomColumn= random.randint(0,numcolumns-1)    
    return randomRow, randomColumn

'''random player that tries to block opponent or win if it notices the possibility
  '@param gameBoard - underlying matrix representing game grid
  '@return coordinates of cell in which player decides to play
  '@calling randomMove, blockOpponent, boardContainsWinner
  '''
def randomMovePlus(gameBoard):
    move= None
    res,winner,pos,direction= glf.boardContainsWinner(gameBoard,3)
    print res
    print winner
    print pos
    print direction
    if res:
        print "BLOCK OR WIN BLOCK OR WIN"
        move= aif.blockOpponent(gameBoard, pos, direction)
        print "block at: "
        print move
    else:
        move= randomMove(gameBoard)
    
    if not move:
        return randomMove(gameBoard)
    else:
        return move

'''random player that blocks opponent or wins if possible
  '@param gameBoard - underlying matrix representing game grid
  '@return coordinates of cell in which player decides to play
  '@calling randomMove, blockOpponent, getSequentialCells
  '''
def randomMovePlus2(gameBoard, playerTurn):
    move= None
    sequentialCells= glf.getSequentialCells(gameBoard,3)
    print "sequential cells are: "
    print sequentialCells
    if playerTurn == 1:
        possibleWins= sequentialCells[1]
        possibleLosses= sequentialCells[2]
    elif playerTurn == 2:
        possibleWins= sequentialCells[2]
        possibleLosses= sequentialCells[1]
        
    print "TRY TO WIN"
    for pos, direction in possibleWins:
        move= aif.blockOpponent(gameBoard, pos, direction)
        if move:
            print "WOOOOOOOONNN, playing: ", move
            break
            
    if not move:
        print "TRY TO BLOCK OPPONENT"
        for pos, direction in possibleLosses:
            move= aif.blockOpponent(gameBoard, pos, direction)
            if move:
                print "BLOCKING OPPONENT, playing: " , move
                break

    if not move:
        print "COULD NOT BLOCK OR WIN, playing random"
        return randomMove(gameBoard)
    else:
        return move