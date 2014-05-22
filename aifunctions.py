import numpy as py
import gamelogicfunctions as glf


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
    print "left: ", left
    print "right: ", right
    if isPlayable( right, gameBoard ):
        return right
    elif isPlayable( left, gameBoard ):
        return left
    print "CANNOT BLOCK"
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
            return (x,y)
    print "Cannot BlockOrWin??? Hm....."

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
                    print "Adding ", r,c ,"to index ", myScores[r,c]
                    print "Removeing ", r,c , "from index ", oldscore
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

'''
  '@param gameBoard1 - one possible future state of the game
  '@param gameBoard2 - one possible future state of the game
  '@playerturn - player 1 or 2
  '@return 1 if gameBoard1 is better for playerTurn than gameBoard2, 
          -1 if gameBoard2 is better,
           0 if cannot determine
  '@calling scoreBoard
  '@caller ai.lookAheadOne
  '''
def isBetterState(gameBoard1, gameBoard2, playerTurn):
    playerScores1, otherScores1, candidateSlots1= scoreBoard(gameBoard1, playerTurn)
    playerScores2, otherScores2, candidateSlots2= scoreBoard(gameBoard2, playerTurn)
    #score myScores boards
    score1= 0
    score2= 0
    numrows,numcolumns= py.shape(playerScores1)
    for r in range(0,numrows):
        for c in range(0, numcolumns):
            if playerScores1[r,c] > playerScores2[r,c]:
                score1+=1
            elif playerScores1[r,c] < playerScores2[r,c]:
                score2+=1
    #score opponent scores
    s1= 0
    s2= 0
    for r in range(0,numrows):
        for c in range(0, numcolumns):
            if playerScores1[r,c] > playerScores2[r,c]:
                s1+=1
            elif playerScores1[r,c] < playerScores2[r,c]:
                s2+=1
    #analyze result and output 1 if first board is better than second board, 0 if even, -1 if second is better than first
    if score1 > s1 and score2 < s2:
        #board1 is better for me AND worse for my opponent
        return 1
    elif s1 > score1 and s2 < score2:
        #board2 is better for me AND worse for my  opponent
        return -1
    elif score1 > s1 or score2 < s2:
        #first board is better for me or worse for my opponent
        return 1
    elif s1 > score1 or s2 < score2:
        #second board is better for me or worse for my opponent
        return -1
    elif score2 > s2 or score1 < s1:
        #second board is better for opponent, worse for me
        return -1
    else:
        return 0
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
b[4,4]= 1

c= py.zeros((6,7))
c[5,4:7]= 1
c[2:5,6]=2
c[5,3]= 2
c[1,6]= 1
c[5,2]= 1
c[2,5]= 1
c[3,5]= 1
c[4,5]= 2
c[4,3]= 1
#cell= randomMovePlusPlus(b)
#valids= getValidMoves(b)
res= isBetterState(b,c,1)'''