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
    if glf.isFull( gameBoard ):
        return 0,0
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
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best local move as determiend by our formula, None otherwise
  '@spec formula: best slot based on scoreBoard
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
            if aif.isSafeToPlay((x,y), yourScores, gameBoard):
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
  '@spec formula: best board based on isBetterState
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
  '@spec formula: best board based on isBetterState
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
  '@spec formula: best board based on isBetterState
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
    print "lookAheadThrice -- yourBestMove ", yourBestMove
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
  '@spec formula: best board based on isSafeToPlay and numb sequentialCells (3)
  '@calling bestLocalMovePlus, aif.getValidMoves, aif.scoreBoard, aif.getOpponent, glf.getSequentialCellsPlus, aif.isSafeToPlay
  '@caller gamePlay
  '''
def lookAheadOnePlus(gameBoard, playerTurn):
    #get all possible moves on gameBoard
    possibleMoves= aif.getValidMoves(gameBoard)
    #get best move based on state of resulting boards
    bestMove, isBlockOrWin= bestLocalMovePlus(gameBoard, playerTurn)
    x,y= bestMove
    #score board for this player and opponent
    myOrScores, yourOrScores, orCandidateSlots= aif.scoreBoard(gameBoard, playerTurn)
    if not aif.isSafeToPlay((x,y), yourOrScores, gameBoard):
        #CAN USE THIS TO PREVENT CONNECT FOUR TRAPS
        print "BEST MOVE IS A LOSS?!?!?!"
    if isBlockOrWin:
        #there cannot be a better play than a block or a win
        print "FOUND IS BLOCK OR WIN FROM BESTLOCALMOVEPLUS"
        return bestMove, isBlockOrWin
    #find the best play that is neither a block or a win
    bestBoard= py.copy(gameBoard)
    bestBoard[bestMove]= playerTurn #py.zeros(py.shape(gameBoard))
    
    opponentTurn= aif.getOpponent(playerTurn)
    for x,y in possibleMoves:
        #play move
        newBoard= py.copy(gameBoard)
        newBoard[x,y]= playerTurn
        oldSequentialCells= glf.getSequentialCellsPlus( bestBoard, 3 )
        oldWinOpportunities= oldSequentialCells[playerTurn]
        oldLoseOpportunities= oldSequentialCells[opponentTurn]
        newSequentialCells= glf.getSequentialCellsPlus( newBoard, 3 )
        newWinOpportunities= newSequentialCells[playerTurn]
        newLoseOpportunities= newSequentialCells[opponentTurn]
        print "let's consider what happens if we played at ", x,y
        #print "oldLoseOpportunities: ", oldLoseOpportunities
        #print "newLoaseOpportunities: ", newLoseOpportunities
        #print "About to compare boards...", len(newWinOpportunities), "vs ", len(oldWinOpportunities)
        print "About to compare boards...", len(newLoseOpportunities), "vs ", len(oldLoseOpportunities)
        #if len(newWinOpportunities) > len(oldWinOpportunities):
        myScores, yourScores, candidateSlots= aif.scoreBoard(newBoard, playerTurn)
        if aif.isSafeToPlay((x,y), yourOrScores, gameBoard) and len(newLoseOpportunities) < len(oldLoseOpportunities):
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
  '@spec formula: best board based on is playable and sequentiallCells (3)
  '@calling lookAheadOnePlus, aif.getValidMoves, aif.scoreBoard, aif.getOpponent,
            glf.getSequentialCellsPlus, aif.isSafeToPlay, aif.isSafeToPlayPlus, aif.preventTrapPlus          
  '@caller gamePlay
  '''
def lookAheadTwicePlus(gameBoard, playerTurn):
    #get all possible moves on gameBoard
    possibleMoves= aif.getValidMoves(gameBoard)
    #get best move based on state of resulting boards
    bestMove, isBlockOrWin= lookAheadOnePlus(gameBoard, playerTurn)
    x,y= bestMove
    #score board for this player and opponent
    myOrScores, yourOrScores, orCandidateSlots= aif.scoreBoard(gameBoard, playerTurn)
    if not aif.isSafeToPlay((x,y), yourOrScores, gameBoard):
        print "lookAheadTwicePlus: -- BEST MOVE IS A LOSS?!?!?!"
    if isBlockOrWin:
        #there cannot be a better play than a block or a win
        print "FOUND IS BLOCK OR WIN FROM BESTLOCALMOVEPLUS"
        return bestMove, isBlockOrWin

    bestBoard= py.copy(gameBoard)
    bestBoard[bestMove]= playerTurn #py.zeros(py.shape(gameBoard))
    trapFlag= 0
    slot= (-1,-1)
    opponentTurn= aif.getOpponent(playerTurn)
    opponentPossibleMoves= aif.getValidMoves(bestBoard)
    for x,y in opponentPossibleMoves:
        print" opoonent move: ", x,y
        temp= py.copy(bestBoard)
        temp[x,y]= opponentTurn
        t, s= aif.preventTrapPlus(gameBoard,bestMove, (x,y), temp, playerTurn)
        print "flag flagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflag ", t
        if t == 1:
            print "WOOOOOOOOOOOOOOOOH PREVENTING TRAAAAAAAAAP IN DEFAULT LOOKAHEADTWICEPLUS ----------------------------"
            print s
            return s, 2
        elif t == -1:
            trapFlag= t
            slot= s
            break
        elif t == 0:
            pass
    #get best move for opponent
    yourBestMove, _= lookAheadOnePlus(bestBoard, opponentTurn)
    bestBoard[yourBestMove]= opponentTurn
    
    
    #trapFlag, slot= aif.preventTrapPlus(gameBoard,bestMove, yourBestMove, bestBoard, playerTurn)
    print "trapflag rapflag rapflag rapflag rapflag rapflag rapflag rapflag rapflag rapflag rapflag rapflag rapflagrapflag ", trapFlag
    '''if trapFlag == 1: 
        print "WOOOOOOOOOOOOOOOOH PREVENTING TRAAAAAAAAAP IN DEFAULT LOOKAHEADTWICEPLUS ----------------------------"
        print slot
        return slot, 2'''
    #find the best play that is neither a block or a win
    for x,y in possibleMoves:
        if trapFlag == -1 and (x,y) == slot:
            print "AVOIDING AVOINDING AVOIDING AVOIDING AVOIDING"
            pass
        else:
            #play move
            newBoard= py.copy(gameBoard)
            newBoard[x,y]= playerTurn
            #get opponent move
            opponentMove, _= lookAheadOnePlus(gameBoard, opponentTurn)
            newBoard[opponentMove]= opponentTurn
            if trapFlag == -1 and bestMove == slot and (x,y) != slot and aif.isSafeToPlayPlus( (x,y), playerTurn, gameBoard ):
                print "REPLACING BAD BEST MOVE ", bestMove, " LEADING TO TRAP WITH ", x,y
                bestMove= (x,y)
                bestBoard= newBoard
                trapFlag= 0
            oldSequentialCells= glf.getSequentialCellsPlus( bestBoard, 3 )
            oldWinOpportunities= oldSequentialCells[playerTurn]
            oldLoseOpportunities= oldSequentialCells[opponentTurn]
            newSequentialCells= glf.getSequentialCellsPlus( newBoard, 3 )
            newWinOpportunities= newSequentialCells[playerTurn]
            newLoseOpportunities= newSequentialCells[opponentTurn]
            #print"About to compare boards...", len(newWinOpportunities), "vs ", len(oldWinOpportunities)
            print "lookAheadTwicePlus ---- let's consider what happens if we played at ", x,y
            print "About to compare boards...", len(newLoseOpportunities), "vs ", len(oldLoseOpportunities)
            #if len(newWinOpportunities) > len(oldWinOpportunities):
            myScores, yourScores, candidateSlots= aif.scoreBoard(newBoard, playerTurn)
            if aif.isSafeToPlay((x,y), yourOrScores, gameBoard) and len(newLoseOpportunities) < len(oldLoseOpportunities):
            #if len(newWinOpportunities) > len(oldWinOpportunities):
                print "FOUND SOMETHING BETTER THAN LOOKAHEADONE: ", x,y
                bestMove= (x,y)
                bestBoard= newBoard
            '''isNewBetter, myScore, yourScore= aif.isBetterState(newBoard, bestBoard, playerTurn)
            if isNewBetter == 1:
                print "FOUND SOMETHING BETTER THAN LOOKAHEADONE: ", x,y
                bestMove= (x,y)
                bestBoard= newBoard'''
    #return move leading to that state
    if trapFlag == -1 and bestMove == slot:
        print "OOOOOOOOOOOOH NOOOOooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo DON'T PLAY THERE"
    return bestMove, isBlockOrWin
    
'''
  '@param gameBoard - underlying matrix representing game grid
  '@param playerTurn - playerID in game 1 or 2)
  '@return best move based on our formula and one look ahead, or random if cannot determine the best one
  '@spec formula: best board based on isPlayable and number of sequentialCells (4) 
  '@calling lookAheadTwicePlus, aif.getValidMoves, aif.scoreBoard, aif.getOpponent, glf.getSequentialCellsPlus, aif.isSafeToPlay
  '@caller gamePlay
  '''
def lookAheadThricePlus(gameBoard, playerTurn):
    #get all possible moves on gameBoard
    possibleMoves= aif.getValidMoves(gameBoard)
    #get best move based on state of resulting boards
    bestMove, isBlockOrWin= lookAheadTwicePlus(gameBoard, playerTurn)
    x,y= bestMove
    #score board for this player and opponent
    myOrScores, yourOrScores, orCandidateSlots= aif.scoreBoard(gameBoard, playerTurn)
    if not aif.isSafeToPlay((x,y), yourOrScores, gameBoard):
        print "lookAheadThricePlus: -- BEST MOVE IS A LOSS?!?!?!"
    if isBlockOrWin:
        #there cannot be a better play than a block or a win
        print "lookAheadThricePlus: --- FOUND IS BLOCK OR WIN FROM BESTLOCALMOVEPLUS"
        return bestMove, isBlockOrWin
    elif isBlockOrWin == 2:
        print "PREVENTION WORKS WITH LOOKAHEADTHRICEPLUS!!!!!!"
        return bestMove, 2

    bestBoard= py.copy(gameBoard)
    bestBoard[bestMove]= playerTurn #py.zeros(py.shape(gameBoard))
    trapFlag= 0
    slot= (-1,-1)
    opponentTurn= aif.getOpponent(playerTurn)
    opponentPossibleMoves= aif.getValidMoves(bestBoard)
    for x,y in opponentPossibleMoves:
        print" opoonent move: ", x,y
        temp= py.copy(bestBoard)
        temp[x,y]= opponentTurn
        t, s= aif.preventTrapPlus(gameBoard,bestMove, (x,y), temp, playerTurn)
        print "flag flagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflag ", t
        if t == 1:
            print "WOOOOOOOOOOOOOOOOH PREVENTING TRAAAAAAAAAP IN DEFAULT LOOKAHEADTHRICEPLUS ----------------------------"
            print s
            return s, 2
        elif t == -1:
            trapFlag= t
            slot= s
            break
        elif t == 0:
            pass
    #get best move for opponent
    yourBestMove, _= lookAheadTwicePlus(bestBoard, opponentTurn)
    bestBoard[yourBestMove]= opponentTurn
    
    myOtherBestMove, _= lookAheadTwicePlus(bestBoard, playerTurn)
    bestBoard[myOtherBestMove]= playerTurn
    
    #find the best play that is neither a block or a win
    for x,y in possibleMoves:
        if (x,y) == slot:
            print "AVOIDING AVOINDING AVOIDING AVOIDING AVOIDING"
            pass
        else:
            #play move
            newBoard= py.copy(gameBoard)
            newBoard[x,y]= playerTurn
            newBoardAfterMyFirstTurn= py.copy(newBoard)
            #get opponent move
            opponentMove, _= lookAheadTwicePlus(gameBoard, opponentTurn)
            newBoard[opponentMove]= opponentTurn
            flag2,slot2= aif.preventTrapPlus(gameBoard, (x,y), opponentMove, newBoard, playerTurn)
            if trapFlag == -1 and flag2 != -1 and aif.isSafeToPlayPlus( (x,y), playerTurn, gameBoard ):
                print "ThricePlus: REPLACING BAD BEST MOVE ", bestMove, " LEADING TO TRAP WITH ", x,y
                bestMove= (x,y)
                bestBoard= newBoard
                trapFlag= 0
            #get my next best move based on this new state
            #TODO if final state has trap or is loss, discard this original move completely. If not, move on to compare this state to the best state seen.
            #TODO check if no traps for opponent but trap for self, then play there
            myMove, _= lookAheadTwicePlus(newBoard, playerTurn)
            newBoard[myMove]= playerTurn
            flag3,slot3= aif.preventTrapPlus(newBoardAfterMyFirstTurn, opponentMove, myMove, newBoard, opponentTurn)
            if flag3 == 1 and aif.isSafeToPlayPlus( slot3, playerTurn, gameBoard ):
                #Trap already active in our favor, use it!
                print "Trap already active in our favor, use it! Trap already active in our favor, use it! Trap already active in our favor, use it! Trap already active in our favor, use it!"
                return slot3
            if flag3 == -1 and aif.isSafeToPlayPlus( slot3, playerTurn, gameBoard ):
                #opponent made a move that activated the trap: consider our move that led to it as a valid place to play
                pass
            if flag2== -1:
                pass
            else:
                oldSequentialCells= glf.getSequentialCellsPlus( bestBoard, 4 )
                oldWinOpportunities= oldSequentialCells[playerTurn]
                oldLoseOpportunities= oldSequentialCells[opponentTurn]
                newSequentialCells= glf.getSequentialCellsPlus( newBoard, 4 )
                newWinOpportunities= newSequentialCells[playerTurn]
                newLoseOpportunities= newSequentialCells[opponentTurn]
                #print"About to compare boards...", len(newWinOpportunities), "vs ", len(oldWinOpportunities)
                print "lookAheadThricePlus ---- let's consider what happens if we played at ", x,y
                print "lookAheadThricePlus ---- About to compare boards...", len(newLoseOpportunities), "vs ", len(oldLoseOpportunities)
                #if len(newWinOpportunities) > len(oldWinOpportunities):
                myScores, yourScores, candidateSlots= aif.scoreBoard(newBoard, playerTurn)
                if aif.isSafeToPlay((x,y), yourOrScores, gameBoard) and len(newLoseOpportunities) < len(oldLoseOpportunities):
                #if len(newWinOpportunities) > len(oldWinOpportunities):
                    print "lookAheadThricePlus ---- FOUND SOMETHING BETTER THAN LOOKAHEADTWICEPLUS: ", x,y
                    bestMove= (x,y)
                    bestBoard= newBoard
                '''isNewBetter, myScore, yourScore= aif.isBetterState(newBoard, bestBoard, playerTurn)
                if isNewBetter == 1:
                    print "FOUND SOMETHING BETTER THAN LOOKAHEADONE: ", x,y
                    bestMove= (x,y)
                    bestBoard= newBoard'''
    #return move leading to that state
    if trapFlag == -1 and bestMove == slot:
        print "OOOOOOOOOOOOH NOOOOooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo DON'T PLAY THERE"
    return bestMove, isBlockOrWin

########################################### START OFFENSIVE PLAYERS ###############################################

'''
  '@param gameBoard - matrix representing game grid
  '@param playerTurn - player making the next move:the caller
  '@return best offensive move to make according to our formula, or random if cannot find one
  '@spec formula: make chains of coins in order to get closer to 4 in a row
  '@calling randomMovePlusPlus, aif.getValidMoves, aif.uselessSlotFilter, 
  '@caller gameplay
  '''
def randomOffense(gameBoard, playerTurn):
    move,isRandom= randomMovePlusPlus( gameBoard, playerTurn )
    if not isRandom:
        print "RandomOffense --- blocking"
        return move, not isRandom
        
    validMoves= aif.getValidMoves( gameBoard )
    filterWorked, validMoves= aif.uselessSlotFilter( gameBoard, validMoves, playerTurn )
    if filterWorked:
        #choose move with higher number
        move= (-1,-1)
        bestVal= -1
        for (x,y,value) in validMoves:
            if value > bestVal:
                move= (x,y)
                bestVal= value
        return move, not isRandom
    #move,isBlockOrWin= lookAheadTwicePlus(gameBoard,playerTurn)
    return move, not isRandom
    '''choice= random.randint( 0, len( validMoves ) - 1 )
    print "RandomOffense --- attacking"
    return validMoves[choice], 0'''

'''
  '@param gameBoard - matrix representing game grid
  '@param playerTurn - player making the next move:the caller
  '@return best offensive move to make according to our formula, or best defensive move from lookAheadTwicePlus
  '@spec formula: make chains of coins in order to get closer to 4 in a row
  '@calling lookAheadTwicePlus, aif.getValidMoves, aif.uselessSlotFilter
  '@caller gameplay
  '''
def randomOffenseWithTwicePlus(gameBoard, playerTurn):
    move,isBlockOrWin= lookAheadTwicePlus(gameBoard,playerTurn)
    if isBlockOrWin == 2 or isBlockOrWin:
        return move, isBlockOrWin
        
    validMoves= aif.getValidMoves( gameBoard )
    filterWorked, validMoves= aif.uselessSlotFilter( gameBoard, validMoves, playerTurn )
    if filterWorked:
        #choose move with higher number
        #move= (-1,-1)
        bestVal= -1
        for (x,y,value) in validMoves:
            if value > 1 and value > bestVal:
                move= (x,y)
                bestVal= value
        return move, 0
    #move,isBlockOrWin= lookAheadTwicePlus(gameBoard,playerTurn)
    return move, 0

'''b= py.zeros((6,7))
(x,y),z= randomOffense(b, 1)'''

'''b= py.zeros((6,7))
b[5,4:7]= 1
b[2:5,6]=2
#x,y= bestLocalMove(b, 1)
#x,y= lookAheadTwice(b, 1)
x,y= lookAheadThrice(b, 1)'''