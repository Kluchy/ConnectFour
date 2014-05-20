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

''' TODO
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
b[0,0:3]= 1
b[1:4,0]= 2
b[4,0]= 2
b[0,4]= 1
b[1,1]= 1
b[2,2]= 1
b[3,3]= 2
b[3:6,6]= 1
#cell= randomMovePlusPlus(b)
valids= getValidMoves(b)'''