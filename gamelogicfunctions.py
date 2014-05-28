#Game Logic Functions
import numpy as py
import matplotlib.pyplot as plt
import gui
#import time


'''
  '@param gameBoard - the back-end matrix representing the board
  '@return true if gameBoard is empty (all 0s), false otherwise
  '@caller
  '''
def isEmpty( gameBoard ):
    shape= py.shape(gameBoard)
    emptyBoard= py.zeros(shape)
    return py.array_equal( gameBoard, emptyBoard )

def isFull( gameBoard ):
    rows,columns= py.shape(gameBoard)
    for c in range(0, columns):
        if gameBoard[0,c] == 0:
            return False
    return True

'''
 '@param y - column corresponding to cell clicked by player
 '@param gameBoard - the back-end matrix representing the board
 '@return true if column y has a free (0.) entry, false otherwise (also if y is out of bounds)
 '@caller gamelogic.gamePlay
 '''
def isMoveValid( y, gameBoard ):
    try:
        column= gameBoard[:,y]
        valid= False
        for cell in column:
            if cell == 0:
                valid= True
        return valid
    except IndexError:
        return False

'''
  '@param gameBoard - the back-end matrix representing the board
  '@return true if gameBoard has a 0 entry, false otherwise
  '@calling isMoveValid
  '@caller gamelogic.gamePlay
  '''
def gameContainsTie(gameBoard):
    isGameTie= True
    numRows,numColumns= py.shape(gameBoard)
    for column in range( 0, numColumns ):
        if isMoveValid( column, gameBoard):
            isGameTie= False;
    return isGameTie

'''
  '@param centerrow, centercolumn - coordinates of starting cell
  '@param rowdirection,columndirection - direction being considered
  '@param iD - length from (centerrow, centercolumn) under consideration
  '@return true if end of vector is out of bounds, false otherwise
  '@caller
  ''' 
def isRangeOutOfBounds(centerrow,centercolumn,rowdirection,columndirection,iD):
    #Helper function isRangeOutOfBounds: returns false if the cells within the
    #vector-range defined by our formula is within the boundaries of the board.
    #true otherwise
    outByRows= ((centerrow + iD*rowdirection) >= gui.NUM_ROWS)  or ((centerrow + iD*rowdirection) < 0)
    outByColumns= ((centercolumn + iD*columndirection) >= gui.NUM_COLUMNS) or ((centercolumn + iD*columndirection) < 0)
    outOfBounds= outByRows or outByColumns
    return outOfBounds

'''
  '@param centerrow, centercolumn - coordinates of starting cell
  '@param rowdirection,columndirection - direction being considered
  '@param sequentialPositionsNeeded - length from (centerrow, centercolumn) under consideration
  '@return true if end of vector is out of bounds, false otherwise
  '@caller
  ''' 
def isRangeOutOfBounds2(centerrow,centercolumn,rowdirection,columndirection, sequentialPositionsNeeded):
    #Helper function isRangeOutOfBounds: returns false if the cells within the
    #vector-range defined by our formula is within the boundaries of the board.
    #true otherwise
    outByRows= (centerrow + (sequentialPositionsNeeded-1)*rowdirection) >= gui.NUM_ROWS  or (centerrow + (sequentialPositionsNeeded-1)*rowdirection) < 0

    outByColumns= (centercolumn + (sequentialPositionsNeeded-1)*columndirection) >= gui.NUM_COLUMNS or (centercolumn + (sequentialPositionsNeeded-1)*columndirection) < 0
    outOfBounds= outByRows or outByColumns
    return outOfBounds
    
'''
  '@param gameBoard - backend matrix for game
  '@param sequentialPositionsNeeded - target number of coins in sequence
  '@param x, y - coordinates of last move played
  '@playerColor - not used
  '@return true if there are 'sequentialPositionsNeeded of coins including one at (x,y), false otherwise
           if true, also returns winner and winning positions
  '@caller gamelogic.gamePlay
  '@calling isRangeOutOfBounds
  '''
def moveYieldsWin( gameBoard, sequentialPositionsNeeded, (x,y), playerColor  ):

    winnerPlayerID= 0;
    winningPositions= py.zeros( ( sequentialPositionsNeeded, 2 ) );

    #directions used for vector manipulations.
    directions= py.array( [ [-1, 1], [0, 1], [1, 1], [1,0] ] );


    numrows,numcolumns= py.shape(gameBoard);
    lastMoveRow= x #y;
    lastMoveColumn= y #x;
    playerID= gameBoard[lastMoveRow,lastMoveColumn];
    solutionFound= False;
    
    #for direct=1:4
    direct= 0;
    while not solutionFound and direct < 4:
        rowdirection= directions[direct,0]
        columndirection= directions[direct, 1]
    #for each possible direction (vertical, horizontal, right and left diagonal), consider the 'sequentialPositionsNeeded' arrangements
    #for p= (-sequentialPositionsNeeded+1):0
        p= -sequentialPositionsNeeded+1
        while not solutionFound and p <= 0:
            #yieldsWin= false;
            #if solution not found and range under consideration is within bounds.
            if not isRangeOutOfBounds(lastMoveRow,lastMoveColumn,rowdirection,columndirection,p) \
                and  not isRangeOutOfBounds(lastMoveRow,lastMoveColumn,rowdirection,columndirection,p+sequentialPositionsNeeded-1):
                yieldsWin= True;
                for iD in range( p, (p+sequentialPositionsNeeded) ):
                #check the next cell within the 'sequentialPositionsNeeded' sequence and see if it equals the original center/playerID under consdieration.
                    if gameBoard[lastMoveRow + iD*rowdirection, lastMoveColumn + iD*columndirection] != playerID:
                        yieldsWin= False;
                    else:
                        winningPositions[iD-p, :]= [lastMoveRow + iD*rowdirection, lastMoveColumn + iD*columndirection];

                if yieldsWin:
                    solutionFound= True;
                    winnerPlayerID= playerID;
                    #update winningPositions
                    for resultRow in range( p, (p+sequentialPositionsNeeded) ):
                        winningPositions[resultRow-p, :]= [lastMoveRow + resultRow*rowdirection, lastMoveColumn + resultRow*columndirection]
                    return solutionFound, winnerPlayerID, winningPositions
                else:
                        winningPositions= py.zeros( ( sequentialPositionsNeeded, 2 ) )

            p= p + 1;  
        direct= direct + 1
    return False, -1, 0

'''
  '@param gameBoard - backend matrix for game
  '@param sequentialPositionsNeeded - target number of coins in sequence
  '@return true if there are 'sequentialPositionsNeeded of coins in sequence in gameBoard, false otherwise
            if true, also returns winner, winning positions and winning direction
  '@caller ai.randomMovePlus
  '@calling isRangeOutOfBounds2
  '''
def boardContainsWinner( gameBoard, sequentialPositionsNeeded ):
    winnerPlayerID= 0;
    winningPositions= py.zeros((sequentialPositionsNeeded,2));
    winningDirection= []
    numrows,numcolumns= py.shape(gameBoard)
    #directions used for vector manipulations.
    directions= py.array([ [-1, 1], [0, 1], [1, 1], [1, 0] ] )
    winnerFound= False;
    #process each cell has endpoint of possible winning sequence.
    row= 0
    while not winnerFound and row < numrows:
        column= 0
        while not winnerFound and column < numcolumns:
            #get value(i.e playerID) and coordinates of cell under consideration.
            playerID= gameBoard[row,column]
            if playerID != 0:
                centerrow= row
                centercolumn= column
                direct= 0
                while not winnerFound and direct < 4:
                    rowdirection= directions[direct,0]
                    columndirection= directions[direct, 1]
                    isCenterWin= False
                    #do nothing if out of bounds
                    if not isRangeOutOfBounds2(centerrow,centercolumn,rowdirection,columndirection,sequentialPositionsNeeded):
                        isCenterWin= True;
                        #otherwise, check the next cell within the 'sequentialPositionsNeeded'
                        #sequence and see if it equals the original center/playerID under consdieration.
                        for iD in range( 0, sequentialPositionsNeeded ):          
                            if gameBoard[centerrow + iD*rowdirection, centercolumn + iD*columndirection] != playerID:
                                isCenterWin= False
                            else:
                                winningPositions[iD, :]= [centerrow + iD*rowdirection, centercolumn + iD*columndirection]

                            #end
                        #end
                    #end
                    if isCenterWin:
                        #return positions of the'sequentialPositionsNeeded' cells and the winner's ID.
                        winnerFound= True
                        winnerPlayerID= playerID
                        winningDirection= [rowdirection, columndirection]
                        return winnerFound, winnerPlayerID, winningPositions, winningDirection
                       #winningPositions(1, :)=[centerrow centercolumn];
                       # for resultRow=1:(sequentialPositionsNeeded-1)
                       #   winningPositions(resultRow+1, :)=[(centerrow + resultRow*rowdirection) (centercolumn + resultRow*columndirection)];
                       #end
                    else:
                        #winnerPlayerID= 0;
                        winningPositions= py.zeros((sequentialPositionsNeeded,2))
                    #end
                    direct= direct + 1
                #end           
            #end
            column= column + 1        
    #end 
        row= row + 1
#end
#here, there are no winners. winnerPlayerID is already 0.
    return False, 0, 0, 0

'''
  '@param gameBoard - backend matrix for game
  '@param sequentialPositionsNeeded - target number of coins in sequence
  '@return a set of 'sequentialPositionsNeeded of coins in sequence in gameBoard as a dictionary
  '@caller ai.randomMovePlus2
  '@calling isRangeOutOfBounds2
  '''
def getSequentialCells( gameBoard, sequentialPositionsNeeded ):
    winnerPlayerID= 0;
    winningPositions= py.zeros((sequentialPositionsNeeded,2));
    winningDirection= []
    sequentialCells= {1:[],2:[]}
    numrows,numcolumns= py.shape(gameBoard)
    #directions used for vector manipulations.
    directions= py.array([ [-1, 1], [0, 1], [1, 1], [1, 0] ] )
    winnerFound= False;
    #process each cell has endpoint of possible winning sequence.
    row= 0
    while not winnerFound and row < numrows:
        column= 0
        while not winnerFound and column < numcolumns:
            #get value(i.e playerID) and coordinates of cell under consideration.
            playerID= gameBoard[row,column]
            if playerID != 0:
                centerrow= row
                centercolumn= column
                direct= 0
                while not winnerFound and direct < 4:
                    rowdirection= directions[direct,0]
                    columndirection= directions[direct, 1]
                    isCenterWin= False
                    #do nothing if out of bounds
                    if not isRangeOutOfBounds2(centerrow,centercolumn,rowdirection,columndirection,sequentialPositionsNeeded):
                        isCenterWin= True;
                        #otherwise, check the next cell within the 'sequentialPositionsNeeded'
                        #sequence and see if it equals the original center/playerID under consdieration.
                        for iD in range( 0, sequentialPositionsNeeded ):          
                            if gameBoard[centerrow + iD*rowdirection, centercolumn + iD*columndirection] != playerID:
                                isCenterWin= False
                            else:
                                winningPositions[iD, :]= [centerrow + iD*rowdirection, centercolumn + iD*columndirection]

                            #end
                        #end
                    #end
                    if isCenterWin:
                        #return positions of the'sequentialPositionsNeeded' cells and the winner's ID.
                        winnerFound= True
                        winnerPlayerID= playerID
                        winningDirection= [rowdirection, columndirection]
                        sequentialCells[winnerPlayerID]= sequentialCells[winnerPlayerID] + [(winningPositions, winningDirection)]
                        winnerFound= False
                        winnerPlayerID= 0
                        winningDirection=[]
                        winningPositions= py.zeros((sequentialPositionsNeeded,2));
                       #winningPositions(1, :)=[centerrow centercolumn];
                       # for resultRow=1:(sequentialPositionsNeeded-1)
                       #   winningPositions(resultRow+1, :)=[(centerrow + resultRow*rowdirection) (centercolumn + resultRow*columndirection)];
                       #end
                    else:
                        #winnerPlayerID= 0;
                        winningPositions= py.zeros((sequentialPositionsNeeded,2))
                    #end
                    direct= direct + 1
                #end           
            #end
            column= column + 1        
    #end 
        row= row + 1
#end
#here, there are no winners. winnerPlayerID is already 0.
    return sequentialCells

'''
  '@param gameBoard - backend matrix for game
  '@param sequentialPositionsNeeded - target number of coins in sequence
  '@return a set of 'sequentialPositionsNeeded of coins (minus 1) in sequence in gameBoard as a dictionary
  '@caller ai.randomMovePlus2
  '@calling isRangeOutOfBounds2
  '''
def getSequentialCellsPlus( gameBoard, sequentialPositionsNeeded ):
    winnerPlayerID= 0;
    winningPositions= py.zeros((sequentialPositionsNeeded,2));
    winningDirection= []
    sequentialCells= {1:[],2:[]}
    numrows,numcolumns= py.shape(gameBoard)
    #directions used for vector manipulations.
    directions= py.array([ [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0] ])
    winnerFound= False;
    #process each cell has endpoint of possible winning sequence.
    row= 0
    while not winnerFound and row < numrows:
        column= 0
        while not winnerFound and column < numcolumns:
            #get value(i.e playerID) and coordinates of cell under consideration.
            playerID= gameBoard[row,column]
            if playerID != 0:
                centerrow= row
                centercolumn= column
                direct= 0
                while not winnerFound and direct < len(directions):
                    rowdirection= directions[direct,0]
                    columndirection= directions[direct, 1]
                    isCenterWin= False
                    #do nothing if out of bounds
                    if not isRangeOutOfBounds2(centerrow,centercolumn,rowdirection,columndirection,sequentialPositionsNeeded):
                        isCenterWin= True;
                        #otherwise, check the next cell within the 'sequentialPositionsNeeded'
                        #sequence and see if it equals the original center/playerID under consdieration.
                        numberMissing= 0
                        for iD in range( 0, sequentialPositionsNeeded ):
                            cellEntry= gameBoard[centerrow + iD*rowdirection, centercolumn + iD*columndirection]          
                            if cellEntry == 0:
                                numberMissing+=1
                                winningPositions[iD, :]= [centerrow + iD*rowdirection, centercolumn + iD*columndirection]
                            elif cellEntry != playerID:
                                isCenterWin= False
                            else:
                                winningPositions[iD, :]= [centerrow + iD*rowdirection, centercolumn + iD*columndirection]
                            if numberMissing > 1:
                                isCenterWin= False

                            #end
                        #end
                    #end
                    if isCenterWin:
                        #return positions of the'sequentialPositionsNeeded' cells and the winner's ID.
                        winnerFound= True
                        winnerPlayerID= playerID
                        winningDirection= [rowdirection, columndirection]
                        sequentialCells[winnerPlayerID]= sequentialCells[winnerPlayerID] + [(winningPositions, winningDirection)]
                        #print sequentialCells
                        winnerFound= False
                        winnerPlayerID= 0
                        winningDirection=[]
                        winningPositions= py.zeros((sequentialPositionsNeeded,2));
                       #winningPositions(1, :)=[centerrow centercolumn];
                       # for resultRow=1:(sequentialPositionsNeeded-1)
                       #   winningPositions(resultRow+1, :)=[(centerrow + resultRow*rowdirection) (centercolumn + resultRow*columndirection)];
                       #end
                    else:
                        #winnerPlayerID= 0;
                        winningPositions= py.zeros((sequentialPositionsNeeded,2))
                    #end
                    direct= direct + 1
                #end           
            #end
            column= column + 1        
    #end 
        row= row + 1
#end
#here, there are no winners. winnerPlayerID is already 0.
    return sequentialCells    

'''
'@param (x,y) - coordinates clicked: x is the column, y is the row
'@param boardHandler - handler for the pyplot object
'@playerColor - color corresponding to 'player'
'@param player - player who clicked in x,y
'@spec updates grid and underlying matrix
'@return coordintes where coin was placed in matrix
'''
def playMove( (x,y), gameBoard, boardHandler, playerColor, player ):
    column= gameBoard[:,x]
    #print "column is: "
    #print column
    
    for i,cell in enumerate(reversed(column)):
        if cell == 0:
            #gameBoard[gui.NUM_ROWS-i-1,y]= player
            gameBoard[gui.NUM_ROWS-i-1,x]= player
            #update GUI
            circle= gui.createCircle( (x + .5,i + .5), playerColor )
            boardHandler.gca().add_artist(circle)
            plt.draw()
            return gui.NUM_ROWS-i-1,x
        
'''#testing yieldsWin
b= py.zeros((6,7))
b[0,0:3]= 1
b[1:4,0]= 2
b[4,0]= 2
b[0,4]= 1
b[1,1]= 1
b[2,2]= 1
b[3,3]= 2
b[5,1:4]= 1
b[3:6,6]= 2
#res,winner,pos= moveYieldsWin(b, 4, (3,0),'r')
#res,winner,pos,direction= boardContainsWinner(b, 4)
cells= getSequentialCellsPlus(b, 2)'''