import numpy as py
import gamelogicfunctions as glf


def getOpponent(playerTurn):
    if playerTurn == 1:
        return 2
    else:
        return 1

'''
  '@param gameBoard - matrix representing game grid
  '@param pos - m X 2 matrix where each row is a grid cell
  '@direction - vectorized direction
  '@return (x,y) coordinates for chosen cell or None if no playable solution
  '@calling isPlayable
  '@caller randomMovePlus, randomMovePlus2
  '''
def blockOpponent(gameBoard, pos, direction):
    left= pos[0]
    right= pos[len(pos)-1]
    left= ( left[0] - direction[0], left[1] - direction[1] )
    right= ( right[0] + direction[0], right[1] + direction[1] )
    #print "left: ", left
    #print "right: ", right
    if isPlayable( right, gameBoard ):
        return right
    elif isPlayable( left, gameBoard ):
        return left
    #print "CANNOT BLOCK"
    return

'''
  '@param gameBoard - matrix representing game grid
  '@param pos - sequentialPosition X 2 array of slots to win or block
  '@return slot (x,y) if playable or None otherwise
  '''
def blockOrWin(gameBoard, pos):
    for row in pos:
        x,y= row[0], row[1]
        if gameBoard[x,y] == 0 and isPlayable( (x,y), gameBoard ):
            print "Blocking/Winning at ", x, y 
            return (x,y)
    #print "Cannot BlockOrWin??? Hm....."

'''
 '@param gameBoard - matrix representing game grid
 '@param playerTurn - 1 or 2
 '@return scores of 'gameBoard' for myself and opponent, and candidate moves
 '@calling glf.getSequentialCellsPlus
 '@caller ai.getLocalMove
 '''
def scoreBoard(gameBoard, playerTurn):
    #2 black copies of board
    myScores= (gameBoard != 0) * (-1)
    #myCandidateSlots= dict()
    yourScores= (gameBoard != 0) * (-1)
    #yourCandidateSlots= dict()
    candidateSlots= dict()
    #for seq=2:4
    sequentialPositions= 2
    limit= 5
    for sequentialPos in range(sequentialPositions,limit):
        sequentialCells= glf.getSequentialCellsPlus(gameBoard, sequentialPos)
        #print "CELLS ARE: ", sequentialCells
        myCells= sequentialCells[playerTurn]
        #print "MY CELLS ARE: ", myCells
        yourCells= sequentialCells[1] if playerTurn == 2 else sequentialCells[2]
        for sequence in  myCells:
            #add sequentialPos to slot == 0
            #print "sequence is : ", sequence
            pos,direction= sequence
            #print "pos is: ", pos
            for row in pos:
                #print "row is: ", row
                r,c= row[0], row[1]
                #print "r,c are: ", r, c
                if gameBoard[r,c] == 0:
                    oldscore= myScores[r,c]
                    myScores[r,c]+= sequentialPos
                    #print "Adding ", r,c ,"to index ", myScores[r,c]
                    #print "Removeing ", r,c , "from index ", oldscore
                    try:
                        candidateSlots[myScores[r,c]]+= [(r,c,playerTurn)]
                    except KeyError:
                        candidateSlots[myScores[r,c]]= [(r,c,playerTurn)]
                        
                    if oldscore != 0:
                        try:
                            candidateSlots[oldscore].remove((r,c,playerTurn))
                        except KeyError:
                            candidateSlots[oldscore]=[]
                        
                    '''try:
                        myCandidateSlots[(r,c)]+= sequentialPos
                    except KeyError:
                        myCandidateSlots[(r,c)]= sequentialPos'''
        for sequence in yourCells:
            pos,direction= sequence
            for row in pos:
                r,c= row[0], row[1]
                if gameBoard[r,c] == 0:
                    oldscore= yourScores[r,c]
                    yourScores[r,c]+= sequentialPos
                    opponentTurn= 1 if playerTurn == 2 else 2
                    try:
                        candidateSlots[yourScores[r,c]]+= [(r,c,opponentTurn)]
                    except KeyError:
                        candidateSlots[yourScores[r,c]]= [(r,c,opponentTurn)]
                        
                    if oldscore != 0:
                        try:
                            candidateSlots[oldscore].remove((r,c,opponentTurn))
                        except KeyError:
                            candidateSlots[oldscore]=[]
                    
                    '''try:
                        yourCandidateSlots[(r,c)]+= sequentialPos
                    except KeyError:
                        yourCandidateSlots[(r,c)]= sequentialPos'''
                    
    return myScores, yourScores, candidateSlots 

def isBetterState(gameBoard1, gameBoard2, playerTurn):
    #return compare(gameBoard1, gameBoard2, playerTurn)
    isWinner, winner, pos, direction= glf.boardContainsWinner( gameBoard1, 4 )
    if isWinner and winner != playerTurn:
        return -1, 0, 0
    elif isWinner and winner == playerTurn:
        return 1, 100, 0
    
    isWinner, winner, pos, direction= glf.boardContainsWinner( gameBoard2, 4 )
    if isWinner and winner != playerTurn:
        return -1, 0, 0
    elif isWinner and winner == playerTurn:
        return 1, 100, 0
    return 0, 0, 0
'''
  '@param gameBoard1 - one possible future state of the game
  '@param gameBoard2 - one possible future state of the game
  '@playerturn - player 1 or 2
  '@return 1 if gameBoard1 is better for playerTurn than gameBoard2, 
          -1 if gameBoard2 is better,
           0 if cannot determine
           + myScore for board and opponentScore for board
  '@calling scoreBoard
  '@caller ai.lookAheadOne
  '@TODO FIND BETTER WAY TO COMPARE TWO BOARDS
  '''
def compare(gameBoard1, gameBoard2, playerTurn):
    playerScores1, otherScores1, candidateSlots1= scoreBoard(gameBoard1, playerTurn)
    playerScores2, otherScores2, candidateSlots2= scoreBoard(gameBoard2, playerTurn)
    #score myScores boards
    score1= 0
    score2= 0
    numrows,numcolumns= py.shape(playerScores1)
    #return 0, score1, score2
    for score in sorted(candidateSlots1.keys(), reverse=True):
        #if score < 4:
          # break
        nextBests= candidateSlots1[score]
        score1= 0
        score2= 0
        for r,c,player in nextBests:
            if player == playerTurn:
                score1+=1
            else:
                score2+=1
    s1= 0
    s2= 0       
    for score in sorted(candidateSlots2.keys(), reverse=True):
        #if score < 4:
          #  break
        nextBests= candidateSlots2[score]
        for r,c,player in nextBests:
            if player == playerTurn:
                s1+=1
            else:
                s2+=1
        '''if score1 > score2:
            return 1, score1, score2
        elif score1 < score2:
            return -1, score1, score2
    return 0, score1, score2'''
                
    '''for score in sorted(candidateSlots1.keys(), reverse=True):
        nextBests= candidateSlots1[score]
        for r,c,player in nextBests:
            if playerScores1[r,c] > otherScores1[r,c]:
                score1+=1
            elif playerScores1[r,c] < otherScores1[r,c]:
                score2+=1
   #score opponent scores
    s1= 0
    s2= 0
    for score in sorted(candidateSlots2.keys(), reverse=True):
        nextBests= candidateSlots2[score]
        for r,c,player in nextBests:
            if otherScores2[r,c] > playerScores2[r,c]:
                s1+=1
            elif otherScores2[r,c] < playerScores2[r,c]:
                s2+=1'''
    #return 0, score1, score2
    '''for r in range(0,numrows):
        for c in range(0, numcolumns):
            if playerScores1[r,c] > otherScores1[r,c]:
                score1+=1
            elif playerScores1[r,c] < otherScores1[r,c]:
                score2+=1
                
    #score opponent scores
    s1= 0
    s2= 0
    for r in range(0,numrows):
        for c in range(0, numcolumns):
            if otherScores2[r,c] > playerScores2[r,c]:
                s1+=1
            elif otherScores2[r,c] < playerScores2[r,c]:
                s2+=1'''
    #analyze result and output 1 if first board is better than second board, 0 if even, -1 if second is better than first
    if score1 > s1 and score2 < s2:
        #board1 is better for me AND worse for my opponent
        return 1, score1, score2
    elif s1 > score1 and s2 < score2:
        #board2 is better for me AND worse for my  opponent
        return -1, score1, score2
    elif score1 > s1 or score2 < s2:
        #first board is better for me or worse for my opponent
        return 1, score1, score2
    elif s1 > score1 or s2 < score2:
        #second board is better for me or worse for my opponent
        return -1, score1, score2
    elif score2 > s2 or score1 < s1:
        #second board is better for opponent, worse for me
        return -1, score1, score2
    else:
        return 0, score1, score2
    
    '''if score1 > score2:
        return 1, score1, score2
    elif score1 < score2:
        return -1, score1, score2
    else:
        return 0, score1, score2'''
    #return score1, score2

'''
  '@param(x,y) - coordinates to cell in gameBoard
  '@param gameBoard - matrix representing game grid
  '@return true if (x,y) is out of bounds, false otherwise
  '@caller isPlayable
  '''
def isOutOfBounds( (x,y), gameBoard ):
    numrows,numcolumns= py.shape(gameBoard)
    outByRows= x >= numrows or x < 0
    outByColumns= y >= numcolumns or y < 0
    isOutOfBounds= outByRows or outByColumns
    return isOutOfBounds

'''
  '@param (x,y) - coordinates to cell in gameBoard
  '@param gameBoard - matrix representing game grid
  '@return true if (x,y) is within bounds, is vacant and (x+1,y) is occupied
  '@caller blockOpponent
  '@calling isOutOfBounds
  '''
def isPlayable( (x,y), gameBoard ):
    numrows,numcolumns= py.shape(gameBoard)
    if isOutOfBounds( (x,y), gameBoard ):
        return False
    elif x+1 == numrows:
        return gameBoard[x,y] == 0
    else:
        return gameBoard[x+1,y] != 0 and gameBoard[x,y] == 0

'''
  '@return true if slot above does not yield to opponent win
  '@caller bestLocalMove, lookAheadOnePlus
  '''
def isSafeToPlay((x,y), opponentScores, gameBoard):
    return opponentScores[x-1,y] < 7 and isPlayable( (x,y), gameBoard )

'''
  '@param (x,y) - coordinates of target slot
  '@param playerTurn - player about to make a move
  '@gameBoard - board state under consideration
  '@calling getOpponent
  '@caller 
  '''
def isSafeToPlayPlus( (x,y), playerTurn, gameBoard):
    temp=py.copy(gameBoard)
    opponentTurn= getOpponent(playerTurn)
    temp[x-1,y]= opponentTurn
    isLoss, _, _= glf.moveYieldsWin(temp, 4, (x-1,y), 'r')
    return not isLoss and isPlayable( (x,y), gameBoard )

'''
  '@param x,y - target move
  '@param TODO TODO TODO TODO TODO refine 
  '@spec return true if x,y allows opponent to win or if future board already has a win for opponent
  '''
def leadsToLoss((x,y)):
    return

'''
  '@param originalBoard - initial state of board before applying myMove and opponentMove
  '@param myMove - move I want to make
  '@param opponentMove - move I Think opponent will make
  '@param futureBoard - new sate of board after applying myMove and opponentMove
  '@param playerTurn - player doing this analysis (so from their perspective
  @calling getOpponent, glf.moveYieldsWin, scoreBoard
  '@caller lookAheadTwicePlus
  '@return (flag, move) where: flag=1 means "play at 'move' to disrupt trap
                                                flag=-1 means "do not play at myMove to avoid activating trap
                                                flag=-2 means "there was a trap but not caused by myMove or opponentMove (shouldnt happen...)
                                                flag=0 means "there is no trap
                                                
   '@note Something was slightly wrong here, so use preventTrapPlus
  '''
def preventTrap(originalBoard, myMove, opponentMove, futureBoard, playerTurn):
    #if futureoard has a trap, find missing slot that will lead to trap and play there.
    #return  flag and that position if it exists and it's possible to play there now. 
    #if exists but not of them are playable yet, return flag and (-1,-1)
    opponentTurn= getOpponent(playerTurn)
    possibleLosses= []
    trapFound= False
    yourOrScores, myOrScores, orCandidateSlots= scoreBoard(originalBoard, opponentTurn)
    yourFScores, myFScores, futureCandidateSlots= scoreBoard(futureBoard, opponentTurn)
    for score in futureCandidateSlots.keys():
        if trapFound:
            break
        if score >= 7:
            #get slots
            loseSlots= futureCandidateSlots[score]
            for slot in loseSlots:
                slotX,slotY,player= slot
                if player != opponentTurn:
                    pass
                elif yourFScores[slotX-1,slotY] >= 7:
                    #this slot and the one above it form a trap
                    temp= py.copy(futureBoard)
                    temp[slotX-1,slotY]= opponentTurn
                    isLoss1, winner1, pos1= glf.moveYieldsWin(temp, 4, (slotX-1,slotY), 'r')
                    temp[slotX-1,slotY]= 0
                    temp[slotX,slotY]= opponentTurn
                    isLoss2, winner2, pos2= glf.moveYieldsWin(temp, 4, (slotX,slotY), 'r')
                    if isLoss1 and isLoss2:
                        trapFound= True
                        print slotX, slotY, " and ", slotX-1,slotY 
                        break
                        
                    #find sequentialPositions leading to a win with this slot
                    #get playable moves on current board
                    #play at a slot that is in intersection of sequentialPositions and playable moves
                elif yourFScores[slotX+1,slotY] >= 7:
                    #this slot and the one below it form a trap
                    temp= py.copy(futureBoard)
                    temp[slotX+1,slotY]= opponentTurn
                    isLoss1, winner1, pos1= glf.moveYieldsWin(temp, 4, (slotX+1,slotY), 'r')
                    temp[slotX+1,slotY]= 0
                    temp[slotX,slotY]= opponentTurn
                    isLoss2, winner2, pos2= glf.moveYieldsWin(temp, 4, (slotX,slotY), 'r')
                    if isLoss1 and isLoss2:
                        trapFound= True
                        print slotX, slotY, " and ", slotX+1,slotY
                        break
                if slot not in possibleLosses:
                    possibleLosses.append(slot)
    if trapFound: 
        myX,myY= myMove
        yourX,yourY= opponentMove
        if isPlayable(opponentMove, originalBoard):
            #then can bprevent trap by playing where opponent would have played
            return 1, opponentMove
        elif myY == yourY and myX == yourX+1:
            #then my move opened up the possibility of a trap: do not play at my move
            return -1, myMove
        else:
            print "preventing trap failed because current moves did not lead to it! What happened..........."
            return -2, myMove 
    else:
        return 0, myMove

'''
  '@param pos1,pos2 - two slots involved in two distinct winning opportunities
  '@param originalBoard - current state of gameBoard
  '@return true if either of pos1 pos2 is playable and the non-playable one depends on the other, false otherwise
  '@caller preventTrapPlus
  '''
def isTrap(pos1, pos2, originalBoard):
    for row1 in pos1:
        for row2 in pos2:
            playable1= isPlayable( (row1[0], row1[1]), originalBoard )
            playable2= isPlayable( (row2[0], row2[1]), originalBoard )
            print "considering ", row1, " and ", row2
            if playable1 and playable2:
                #those two slots do not depend on each other
                print" well........"
                pass
            if not playable2:
                #see if 2 depends on 1
                temp= py.copy(originalBoard)
                temp[row1[0],row1[1]]= 3
                if isPlayable( (row2[0], row2[1]), temp ):
                    #2 depends on 1
                    return True
            if not playable1:
                #see if 1 depends on 2
                temp= py.copy(originalBoard)
                temp[row2[0],row2[1]]= 3
                if isPlayable( (row1[0], row1[1]), temp ):
                    #1 depends on 2
                    return True
            else:
                print "should not go in here"
                pass
    return False
    
'''
  '@param originalBoard - initial state of board before applying myMove and opponentMove
  '@param myMove - move I want to make
  '@param opponentMove - move I Think opponent will make
  '@param futureBoard - new sate of board after applying myMove and opponentMove
  '@param playerTurn - player doing this analysis (so from their perspective
  @calling getOpponent, glf.moveYieldsWin, scoreBoard, isTrap
  '@caller lookAheadTwicePlus
  '@return (flag, move) where: flag=1 means "play at 'move' to disrupt trap
                                                flag=-1 means "do not play at myMove to avoid activating trap
                                                flag=0 means "there is no trap
                                                
   '@note logic fix from preventTrap
  '''
def preventTrapPlus(originalBoard, myMove, opponentMove, futureBoard, playerTurn):
    #if futureoard has a trap, find missing slot that will lead to trap and play there.
    #return  flag and that position if it exists and it's possible to play there now. 
    #print "IN"
    #if exists but not of them are playable yet, return flag and (-1,-1)
    opponentTurn= getOpponent(playerTurn)
    possibleLosses= []
    traps= []
    trapFound= False
    possibleBadMoves= py.zeros((0,0))
    yourOrScores, myOrScores, orCandidateSlots= scoreBoard(originalBoard, opponentTurn)
    yourFScores, myFScores, futureCandidateSlots= scoreBoard(futureBoard, opponentTurn)
    for score in futureCandidateSlots.keys():
        #if trapFound:
         #   break
        if score >= 7:
            #get slots
            loseSlots= futureCandidateSlots[score]
            for slot in loseSlots:
                slotX,slotY,player= slot
                if player != opponentTurn:
                    print" ok"
                    pass
                else:
                    print"this is for opponent"
                    temp= py.copy(futureBoard)
                    temp[slotX,slotY]= opponentTurn
                    isLoss2, winner2, pos2= glf.moveYieldsWin(temp, 4, (slotX,slotY), 'r')
                    print isLoss2
                    if isLoss2:
                        #check if any pair seen thus far are actually part of a trap
                        for ((x,y),pos) in possibleLosses:
                            print "loop"
                            print "comparing ", pos , " with  ", pos2
                            if isTrap(pos, pos2, originalBoard):
                                traps.append(  [ ( (x,y),pos ),( (slotX,slotY),pos2 ) ] )
                                trapFound= True
                                possibleBadMoves= py.append( possibleBadMoves, pos )
                                possibleBadMoves= py.append( possibleBadMoves, pos2 )
                                #break
                        possibleLosses.append( ((slotX,slotY), pos2) )

                #if len(possibleLosses) > 1:
                 #   trapFound= True
                  #  break
                '''elif yourFScores[slotX-1,slotY] >= 7:
                    #this slot and the one above it form a trap
                    temp= py.copy(futureBoard)
                    temp[slotX-1,slotY]= opponentTurn
                    isLoss1, winner1, pos1= glf.moveYieldsWin(temp, 4, (slotX-1,slotY), 'r')
                    temp[slotX-1,slotY]= 0
                    temp[slotX,slotY]= opponentTurn
                    isLoss2, winner2, pos2= glf.moveYieldsWin(temp, 4, (slotX,slotY), 'r')
                    if isLoss1 and isLoss2:
                        trapFound= True
                        print slotX, slotY, " and ", slotX-1,slotY 
                        break
                        
                    #find sequentialPositions leading to a win with this slot
                    #get playable moves on current board
                    #play at a slot that is in intersection of sequentialPositions and playable moves
                elif yourFScores[slotX+1,slotY] >= 7:
                    #this slot and the one below it form a trap
                    temp= py.copy(futureBoard)
                    temp[slotX+1,slotY]= opponentTurn
                    isLoss1, winner1, pos1= glf.moveYieldsWin(temp, 4, (slotX+1,slotY), 'r')
                    temp[slotX+1,slotY]= 0
                    temp[slotX,slotY]= opponentTurn
                    isLoss2, winner2, pos2= glf.moveYieldsWin(temp, 4, (slotX,slotY), 'r')
                    if isLoss1 and isLoss2:
                        trapFound= True
                        print slotX, slotY, " and ", slotX+1,slotY
                        break'''
                #if slot not in possibleLosses:
                 #   possibleLosses.append(slot)
    if trapFound: 
        myX,myY= myMove
        yourX,yourY= opponentMove
        for pair in traps:
            for ((x,y), pos) in pair:
                for row in pos:
                    print "checking for prevention block: ", row[0], row[1]
                    if isSafeToPlayPlus( (row[0],row[1]), playerTurn, originalBoard):
                        return 1, (row[0],row[1])
        #before returning, check if myMove is involved in any traps
        #how to check if move involved in trap? 
        #1----if removing it from futureBoard does not change numTraps found
        possibleBadMoves= py.reshape(possibleBadMoves, (len(possibleBadMoves)/2,2))
        for row in possibleBadMoves:
            if (myX-1, myY) == (row[0], row[1]):
                return -1, myMove
        return 0, myMove
        '''if isPlayable(opponentMove, originalBoard):
            #then can bprevent trap by playing where opponent would have played
            return 1, opponentMove
        elif myY == yourY and myX == yourX+1:
            #then my move opened up the possibility of a trap: do not play at my move
            return -1, myMove
        else:
            print "preventing trap failed because current moves did not lead to it! What happened..........."
            return -2, myMove '''
    else:
        return 0, myMove


'''
  '@param y - integer reresenting column of gameBoard
  '@param gameBoard - matrix representing game grid
  '@return first playable row in column 'y' or -1 if 'y' is full
  '@caller
  '@calling
  '''
def getNextColumnMove(y,gameBoard):
    column= gameBoard[:,y]
    for x,entry in enumerate(reversed(column)):
        if entry == 0:
            return x
    return -1

'''
  '@param gameBoard - matrix representing game grid
  '@return playable cells from gameBoard in list
  '@caller
  '@calling
  '''
def getValidMoves(gameBoard):
    validMoves= []
    numrows, numcolumns= py.shape(gameBoard)
    for column in range(0, numcolumns):
        for row in range(0, numrows):
            valid= gameBoard[numrows- row- 1,column]
            if valid == 0:
                validMoves= validMoves + [(numrows-row-1, column)]
                break
    return validMoves

'''
  '''
def moveYieldsPossibleWin( gameBoard, sequentialPositionsNeeded, (x,y), playerTurn  ):

    numPlayerIDs= 0;
    winningPositions= py.zeros( ( sequentialPositionsNeeded, 2 ) );

    #directions used for vector manipulations.
    directions= py.array( [ [-1, 1], [0, 1], [1, 1] ] );


    numrows,numcolumns= py.shape(gameBoard);
    lastMoveRow= x #y;
    lastMoveColumn= y #x;
    playerID= playerTurn;
    solutionFound= False;
    
    #for direct=1:4
    direct= 0;
    while not solutionFound and direct < 3:
        rowdirection= directions[direct,0]
        columndirection= directions[direct, 1]
    #for each possible direction (vertical, horizontal, right and left diagonal), consider the 'sequentialPositionsNeeded' arrangements
    #for p= (-sequentialPositionsNeeded+1):0
        p= -sequentialPositionsNeeded+1
        while not solutionFound and p <= 0:
            #yieldsWin= false;
            #if solution not found and range under consideration is within bounds.
            if not glf.isRangeOutOfBounds(lastMoveRow,lastMoveColumn,rowdirection,columndirection,p) \
                and  not glf.isRangeOutOfBounds(lastMoveRow,lastMoveColumn,rowdirection,columndirection,p+sequentialPositionsNeeded-1):
                yieldsWin= True;
                for iD in range( p, (p+sequentialPositionsNeeded) ):
                #check the next cell within the 'sequentialPositionsNeeded' sequence and see if it equals the original center/playerID under consdieration.
                    cell= gameBoard[lastMoveRow + iD*rowdirection, lastMoveColumn + iD*columndirection]
                    if  cell != playerID and cell != 0:
                        yieldsWin= False;
                        numPlayerIDs= 0
                    else:
                        winningPositions[iD-p, :]= [lastMoveRow + iD*rowdirection, lastMoveColumn + iD*columndirection];
                        if cell == playerID:
                            numPlayerIDs+=1

                if yieldsWin:
                    solutionFound= True;
                    #numPlayerIDs= playerID;
                    #update winningPositions
                    for resultRow in range( p, (p+sequentialPositionsNeeded) ):
                        winningPositions[resultRow-p, :]= [lastMoveRow + resultRow*rowdirection, lastMoveColumn + resultRow*columndirection]
                    return solutionFound, numPlayerIDs, winningPositions, directions[direct]
                else:
                        winningPositions= py.zeros( ( sequentialPositionsNeeded, 2 ) )

            p= p + 1;  
        direct= direct + 1
    return False, -1, 0, []

'''
  '@param gameBoard - matrix representing game grid
  '@param validMoves - list of coordinates  that are valid moves for the current turn
  '@param playerTurn - current player
  '@return validMoves without slots that cannot contribute to a future win for playerTurn
  '''
def uselessSlotFilter(gameBoard, validMoves, playerTurn):
    filteredMoves= []
    for (x,y) in validMoves:
        #get new sequentialCells to determine free spaces around this slot
        isPossibleWin, numPlayerIDs, pos, winningDirection= moveYieldsPossibleWin( gameBoard, 4, (x,y), playerTurn )
        #if x y has at least one chance of turning into a win, add to list.
        if isPossibleWin:
            filteredMoves.append( ( x, y ) )
            
    if len(filteredMoves) == 0:
        print "uselessSlotFilter --- no good attacking positions"
        return validMoves
    else:
        print "uselessSlotFilter --- attacking positions: ", filteredMoves
        return filteredMoves
    

'''#testing randomMove
b= py.zeros((6,7))

b[5,4:7]= 1
b[2:5,6]=2
b[5,3]= 2
b[1,6]= 1
b[5,2]= 1
b[2,5]= 1
b[3,5]= 1
b[4,5]= 2
b[4,4]= 1'''

'''c= py.zeros((6,7))
c[5,4:7]= 1
c[2:5,6]=2
c[5,3]= 2
c[1,6]= 1
c[5,2]= 1
c[2,5]= 1
c[3,5]= 1
c[4,5]= 2
c[4,3]= 1
c[4,0:3]= 2
c[3,2:4]= 2
c2=py.copy(c)
c[2,2:4]= 1
c2[2,2]= 1
c2[3,3]= 0
res= preventTrap( c2, (3,3), (2,3), c, 2)
resp= preventTrapPlus( c2, (3,3), (2,3), c, 2)'''

#cell= randomMovePlusPlus(b)
#valids= getValidMoves(b)
#res= isBetterState(b,c,1)
