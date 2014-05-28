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
    randomRow= 5 #random.randint(0,numrows-1)
    randomColumn= random.randint(0,numcolumns-1)
    while not glf.isMoveValid( randomColumn, gameBoard):
        #randomRow= random.randint(0,numrows-1)
        randomColumn= random.randint(0,numcolumns-1)   
    print "playing randomly at " ,randomRow, randomColumn 
    return randomRow, randomColumn

'''random player that tries to block opponent or win if it notices the possibility
  '@param gameBoard - underlying matrix representing game grid
  '@return coordinates of cell in which player decides to play
  '@calling randomMove, blockOpponent, boardContainsWinner
  '''
def randomMovePlus(gameBoard):
    move= None
    res,winner,pos,direction= glf.boardContainsWinner(gameBoard,3)
    #print res
    #print winner
    #print pos
    #print direction
    if res:
        #print "BLOCK OR WIN BLOCK OR WIN"
        move= aif.blockOpponent(gameBoard, pos, direction)
        #print "block at: "
        #print move
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
    #print "sequential cells are: "
    #print sequentialCells
    if playerTurn == 1:
        possibleWins= sequentialCells[1]
        possibleLosses= sequentialCells[2]
    elif playerTurn == 2:
        possibleWins= sequentialCells[2]
        possibleLosses= sequentialCells[1]
        
    #print "TRY TO WIN"
    for pos, direction in possibleWins:
        move= aif.blockOpponent(gameBoard, pos, direction)
        if move:
            #print "WOOOOOOOONNN, playing: ", move
            break
            
    if not move:
        #print "TRY TO BLOCK OPPONENT"
        for pos, direction in possibleLosses:
            move= aif.blockOpponent(gameBoard, pos, direction)
            if move:
                #print "BLOCKING OPPONENT, playing: " , move
                break

    if not move:
        #print "COULD NOT BLOCK OR WIN, playing random"
        return randomMove(gameBoard)
    else:
        return move
        
'''random player that blocks opponent or wins if possible
  '@param gameBoard - underlying matrix representing game grid
  '@return coordinates of cell in which player decides to play, and a flag for randomness
  '@calling randomMove, blockOpponent, getSequentialCells
  '@caller gamePlay, bestLocalMovePlus
  '''
def randomMovePlusPlus(gameBoard, playerTurn):
    move= None
    sequentialCells= glf.getSequentialCellsPlus(gameBoard,4)
    #print "sequential cells are: "
    #print sequentialCells
    if playerTurn == 1:
        possibleWins= sequentialCells[1]
        possibleLosses= sequentialCells[2]
    elif playerTurn == 2:
        possibleWins= sequentialCells[2]
        possibleLosses= sequentialCells[1]
        
    #print "TRY TO WIN"
    for pos, direction in possibleWins:
        move= aif.blockOrWin(gameBoard, pos)
        if move:
            #print "WOOOOOOOONNN, playing: ", move
            break
            
    if not move:
        #print "TRY TO BLOCK OPPONENT"
        for pos, direction in possibleLosses:
            move= aif.blockOrWin(gameBoard, pos)
            if move:
                #print "BLOCKING OPPONENT, playing: " , move
                break

    if not move:
        #print "COULD NOT BLOCK OR WIN, playing random"
        return randomMove(gameBoard),1
    else:
        return move,0
    
'''
  '@return true if slot above does not yield to opponent win
  '@caller bestLocalMove, lookAheadOnePlus
  '''
def isSafeToPlay((x,y), opponentScores, gameBoard):
    return opponentScores[x-1,y] < 7 and aif.isPlayable( (x,y), gameBoard )

'''
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best local move as determiend by our formula, None otherwise
  '@calling aif.scoreBoard, aif.isPlayable
  '@caller bestLocalMovePlus, gamePlay
  '''
def bestLocalMove(gameBoard, playerTurn):
    #score board for this player and opponent
    myScores, yourScores, candidateSlots= aif.scoreBoard(gameBoard, playerTurn)
    #get positions
    for score in sorted(candidateSlots.keys(), reverse=True):
        nextBests= candidateSlots[score]
        for x,y,player in nextBests:
            if isSafeToPlay((x,y), yourScores, gameBoard):
                return x,y
            else:
                #print "CANNOT PLAY AT ", x, y,"-----------------------------------"
                pass
    #return myScores, yourScores,candidateSlots

'''
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best move based on ourformula and current state, or random if cannot determine the best one
  '@calling randomPlusPlus, bestLocalMove
  '@caller gamePlay
  '@TODO ONLY RETURN TRUE WHEN RANDOMMOVEPLUS RETURNS BLOCKORWIN
  '''
def bestLocalMovePlus(gameBoard, playerTurn):
    move,isRandom= randomMovePlusPlus(gameBoard, playerTurn)
    if isRandom:
        best= bestLocalMove(gameBoard, playerTurn)
        if best:
            print "bestLocalMovePlus: ", best
            return best, not isRandom
        else:
            #print "GOING TO PLAY RANDOMLY"
            return move, not isRandom
    else:
        #print "NOT RANDDOM BUUUUUUUUUUUUUUUT"
        print "bestLocalMovePlus Block Or Win: ", move
        return move, not isRandom

'''
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best move based on our formula and one look ahead, or random if cannot determine the best one 
  '@calling bestLocalMovePlus, aif.isBetterState, aif.getValidMoves
  '@caller gamePlay
  '''
def lookAheadOne(gameBoard, playerTurn):
    #get all possible moves on gameBoard
    possibleMoves= aif.getValidMoves(gameBoard)
    #get best move based on state of resulting boards
    bestMove, isBlockOrWin= bestLocalMovePlus(gameBoard, playerTurn)
    if isBlockOrWin:
        #there cannot be a better play than a block or a win
        print "FOUND IS BLOCK OR WIN FROM BESTLOCALMOVEPLUS"
        return bestMove, isBlockOrWin
    #find the best play that is neither a block or a win
    bestBoard= py.copy(gameBoard)
    bestBoard[bestMove]= playerTurn #py.zeros(py.shape(gameBoard))
    for x,y in possibleMoves:
        #play move
        newBoard= py.copy(gameBoard)
        newBoard[x,y]= playerTurn
        isNewBetter, myScore, yourScore= aif.isBetterState(newBoard, bestBoard, playerTurn)
        if isNewBetter == 1:
            print "FOUND SOMETHING BETTER THAN BESTLOCALMOVEPLUS: ", x,y
            bestMove= (x,y)
            bestBoard= newBoard
    #return move leading to that state
    return bestMove, isBlockOrWin

'''
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best move based on our formula and two look aheads, or random if cannot determine the best one
  '@calling lookAheadOne, aif.getValidMoves, aif.getOpponent, aif.isBetterState
  '@caller lookAheadThrice
  '''
def lookAheadTwice(gameBoard, playerTurn):
    #get all possible moves on gameBoard
    possibleMoves= aif.getValidMoves(gameBoard)
    #get best move based on state of resulting boards
    myBestMove, isBlockOrWin= lookAheadOne(gameBoard, playerTurn)
    if isBlockOrWin:
        print "FOUND IS BLOCK OR WIN FROM LOOKAHEADONE"
        return myBestMove, isBlockOrWin
    bestBoard= py.copy(gameBoard) #board state after opponent makes a move
    #play my best move based on local state
    bestBoard[myBestMove]= playerTurn
    opponentTurn= aif.getOpponent(playerTurn)
    yourBestMove, _= lookAheadOne(bestBoard, opponentTurn)
    #play opponent's best move based on local state
    bestBoard[yourBestMove]= opponentTurn
    
    for x,y in possibleMoves:
        #play move
        newBoard= py.copy(gameBoard)
        newBoard[x,y]= playerTurn
        #get opponent's best move based on this new state

        opponentMove, _= lookAheadOne(newBoard, opponentTurn)
        opponentBoard= py.copy(newBoard)
        opponentBoard[opponentMove]= opponentTurn
        #score state opponent led to
        isNewBetter, myScore, yourScore= aif.isBetterState(opponentBoard, bestBoard, opponentTurn)
        if isNewBetter == 1:
            print "FOUND SOMETHING BETTER THAN lookAheadOne: ", x,y
            myBestMove= (x,y)
            bestBoard= opponentBoard
            yourBestMove= opponentMove
            
    return myBestMove, isBlockOrWin

'''
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best move based on our formula and two look aheads, or random if cannot determine the best one
  '@calling lookAheadOne, lookAheadTwice, aif.getValidMoves, aif.getOpponent, aif.isBetterState
  '@caller gamePlay
  '''
def lookAheadThrice(gameBoard, playerTurn):
    #get all possible moves on gameBoard
    possibleMoves= aif.getValidMoves(gameBoard)
    #get best move based on state of resulting boards
    myBestMove, isBlockOrWin= lookAheadTwice(gameBoard, playerTurn)
    if isBlockOrWin:
        print "NOT GONNA BOTHER, FOUND BLOCK OR WIN"
        return myBestMove, isBlockOrWin
    bestBoard= py.copy(gameBoard)
    #play my best move based on local state
    bestBoard[myBestMove]= playerTurn
    opponentTurn= aif.getOpponent(playerTurn)
    yourBestMove, _= lookAheadTwice(bestBoard, opponentTurn)
    print "lookAheadThrice: ", yourBestMove
    #play opponent's best move based on local state
    bestBoard[yourBestMove]= opponentTurn
    myOtherBestMove, _= lookAheadTwice(bestBoard, playerTurn)
    bestBoard[myOtherBestMove]= playerTurn
    
    for x,y in possibleMoves:
        #play move
        newBoard= py.copy(gameBoard)
        newBoard[x,y]= playerTurn
        #get opponent's best move based on this new state

        opponentMove, _= lookAheadTwice(newBoard, opponentTurn)
        newBoard[opponentMove]= opponentTurn
        #get my next best move based on this new state
        myMove, _= lookAheadOne(newBoard, playerTurn)
        newBoard[myMove]= playerTurn
        #score this 'final' state
        isNewBetter, myScore, yourScore= aif.isBetterState(newBoard, bestBoard, playerTurn)
        print  isNewBetter, myScore, yourScore
        if isNewBetter == 1:
            print "FOUND SOMETHING BETTER THAN lookAheadTwice: ", x,y
            bestBoard= newBoard
            myBestMove= (x,y)
    
    return myBestMove, not isBlockOrWin
    
'''
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best move based on our formula and one look ahead, or random if cannot determine the best one 
  '@calling bestLocalMovePlus, aif.getValidMoves
  '@caller gamePlay
  '''
def lookAheadOnePlus(gameBoard, playerTurn):
    #get all possible moves on gameBoard
    possibleMoves= aif.getValidMoves(gameBoard)
    #get best move based on state of resulting boards
    bestMove, isBlockOrWin= bestLocalMovePlus(gameBoard, playerTurn)
    x,y= bestMove
    #score board for this player and opponent
    myScores, yourScores, candidateSlots= aif.scoreBoard(gameBoard, playerTurn)
    if not isSafeToPlay((x,y), yourScores, gameBoard):
        print "BEST MOVE IS A LOSS?!?!?!"
    if isBlockOrWin:
        #there cannot be a better play than a block or a win
        print "FOUND IS BLOCK OR WIN FROM BESTLOCALMOVEPLUS"
        return bestMove, isBlockOrWin
    #find the best play that is neither a block or a win
    bestBoard= py.copy(gameBoard)
    bestBoard[bestMove]= playerTurn #py.zeros(py.shape(gameBoard))
    for x,y in possibleMoves:
        #play move
        newBoard= py.copy(gameBoard)
        newBoard[x,y]= playerTurn
        oldSequentialCells= glf.getSequentialCellsPlus( bestBoard, 2 )
        oldWinOpportunities= oldSequentialCells[1]
        oldLoseOpportunities= oldSequentialCells[2]
        newSequentialCells= glf.getSequentialCellsPlus( newBoard, 2 )
        newWinOpportunities= newSequentialCells[1]
        newLoseOpportunities= newSequentialCells[2]
        #print "About to compare boards...", len(newWinOpportunities), "vs ", len(oldWinOpportunities)
        print "About to compare boards...", len(newLoseOpportunities), "vs ", len(oldLoseOpportunities)
        #if len(newWinOpportunities) > len(oldWinOpportunities):
        myScores, yourScores, candidateSlots= aif.scoreBoard(newBoard, playerTurn)
        if isSafeToPlay((x,y), yourScores, gameBoard) and len(newLoseOpportunities) < len(oldLoseOpportunities):
            print "FOUND SOMETHING BETTER THAN BESTLOCALMOVEPLUS: ", x,y
            bestMove= (x,y)
            bestBoard= newBoard
        '''isNewBetter, myScore, yourScore= aif.isBetterState(newBoard, bestBoard, playerTurn)
        if isNewBetter == 1:
            print "FOUND SOMETHING BETTER THAN BESTLOCALMOVEPLUS: ", x,y
            bestMove= (x,y)
            bestBoard= newBoard'''
    #return move leading to that state
    return bestMove, isBlockOrWin
    
    
'''
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best move based on our formula and one look ahead, or random if cannot determine the best one 
  '@calling lookAheadOnePlus, aif.getValidMoves
  '@caller gamePlay
  '''
def lookAheadTwicePlus(gameBoard, playerTurn):
    #get all possible moves on gameBoard
    possibleMoves= aif.getValidMoves(gameBoard)
    #get best move based on state of resulting boards
    bestMove, isBlockOrWin= lookAheadOnePlus(gameBoard, playerTurn)
    x,y= bestMove
    #score board for this player and opponent
    myScores, yourScores, candidateSlots= aif.scoreBoard(gameBoard, playerTurn)
    if not isSafeToPlay((x,y), yourScores, gameBoard):
        print "lookAheadTwicePlus: -- BEST MOVE IS A LOSS?!?!?!"
    if isBlockOrWin:
        #there cannot be a better play than a block or a win
        print "FOUND IS BLOCK OR WIN FROM BESTLOCALMOVEPLUS"
        return bestMove, isBlockOrWin

    bestBoard= py.copy(gameBoard)
    bestBoard[bestMove]= playerTurn #py.zeros(py.shape(gameBoard))
    #get best move for opponent
    opponentTurn= aif.getOpponent(playerTurn)
    yourBestMove, _= lookAheadOnePlus(bestBoard, opponentTurn)
    bestBoard[yourBestMove]= opponentTurn
    #find the best play that is neither a block or a win
    for x,y in possibleMoves:
        #play move
        newBoard= py.copy(gameBoard)
        newBoard[x,y]= playerTurn
        #get opponent move
        opponentMove, _= lookAheadOnePlus(gameBoard, opponentTurn)
        newBoard[opponentMove]= opponentTurn
        
        oldSequentialCells= glf.getSequentialCellsPlus( bestBoard, 3 )
        oldWinOpportunities= oldSequentialCells[1]
        oldLoseOpportunities= oldSequentialCells[2]
        newSequentialCells= glf.getSequentialCellsPlus( newBoard, 3 )
        newWinOpportunities= newSequentialCells[1]
        newLoseOpportunities= newSequentialCells[2]
        #print "About to compare boards...", len(newWinOpportunities), "vs ", len(oldWinOpportunities)
        print "About to compare boards...", len(newLoseOpportunities), "vs ", len(oldLoseOpportunities)
        #if len(newWinOpportunities) > len(oldWinOpportunities):
        myScores, yourScores, candidateSlots= aif.scoreBoard(newBoard, playerTurn)
        if isSafeToPlay((x,y), yourScores, gameBoard) and len(newLoseOpportunities) < len(oldLoseOpportunities):
        #if len(newWinOpportunities) > len(oldWinOpportunities):
            print "FOUND SOMETHING BETTER THAN BESTLOCALMOVEPLUS: ", x,y
            bestMove= (x,y)
            bestBoard= newBoard
        '''isNewBetter, myScore, yourScore= aif.isBetterState(newBoard, bestBoard, playerTurn)
        if isNewBetter == 1:
            print "FOUND SOMETHING BETTER THAN BESTLOCALMOVEPLUS: ", x,y
            bestMove= (x,y)
            bestBoard= newBoard'''
    #return move leading to that state
    return bestMove, isBlockOrWin
    
'''b= py.zeros((6,7))
b[5,4:7]= 1
b[2:5,6]=2
#x,y= bestLocalMove(b, 1)
#x,y= lookAheadTwice(b, 1)
x,y= lookAheadThrice(b, 1)'''