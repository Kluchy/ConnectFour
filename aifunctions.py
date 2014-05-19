import numpy as py

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
  '@return playable cells form gameBoard
  '@caller
  '@calling
  '''
def getValidMoves(gameBoard):
    #validMoves= 
    numrows, numcolumns= py.shape(gameBoard)
    for column in range(0, numcolumns):
        return
        
#testing randomMove
'''b= py.zeros((6,7))
b[0,0:3]= 1
b[1:4,0]= 2
b[4,0]= 2
b[0,4]= 1
b[1,1]= 1
b[2,2]= 1
b[3,3]= 2
b[3:6,6]= 1
cell= randomMovePlus(b)'''