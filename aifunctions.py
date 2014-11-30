import numpy as py
import gamelogicfunctions as glf
from operator import itemgetter


class Node:
    '''
      '@field board - 6X7 matrix of a board game
      '@field move - (x,y) coordinates of slot played by 'playerturn'
      '@field parentNode - the Node representing this board's ancestor (this board - move at 'move')
      '@field playerTurn - the player who created this board by playing at 'move'
      '@field isLeaf - True if this node is a leaf in our game tree snapshot
      '@field self.value - score for this board based on a scoring function
      '''
    def __init__(self, board, move, parentNode, playerTurn, isLeaf=False):
        self.parentNode= parentNode
        self.board= board
        self.isLeaf= isLeaf
        self.playerTurn= playerTurn
        self.value= 0.0
        self.move= move

class Tree:
    '''
      '@field structure - dictionary containing our game tree with root at key '0'.
                         mapping [parentNode] => list of children Nodes
      '@field leafNodes - a list of all the leaf nodes in this tree
      '@field trainPlies - training data of partial boards and labels (win/loss/draw)
      '''
    def __init__(self, startBoard, numTurns, trainPlies, playerTurn, scoringFunc):
        self.structure= dict()
        self.leafNodes= []
        self.trainPlies= trainPlies
        self.structure[0]= Node( startBoard,(None,None), None, playerTurn )
        self.createGameTree( self.structure[0], numTurns, playerTurn )
        if scoringFunc == "knn":
            self.scoreTree( playerTurn )
        elif scoringFunc == "getSequentialCellsPlus":
            self.scoreTreeWithSeqCellsPlus( playerTurn )
        
    '''
      '@param startBoard - starting board state
      '@param numTurns - cutoff depth of game tree
      '@param playerturn - player making the analysis
      '@spec creates a game tree of depth numturns
      '@void
      '''
    def createGameTree(self, startBoard, numTurns, playerTurn ):
        if numTurns == 0:
            #give score to current leaf 'startBoard'
            return
        else:
            validMoves= getValidMoves( startBoard.board )
            for (x,y) in validMoves:
                nextBoard= py.copy(startBoard.board)
                nextBoard[x,y]= playerTurn
                if numTurns - 1 == 0:
                    nextBoard= Node( nextBoard, (x,y), startBoard, playerTurn, isLeaf=True )
                    self.leafNodes.append( nextBoard )
                else:
                    nextBoard= Node( nextBoard, (x,y), startBoard, playerTurn )
                try:
                    self.structure[startBoard].append( nextBoard )
                except KeyError:
                    self.structure[startBoard]= [ nextBoard ]
                self.createGameTree( nextBoard, numTurns-1, getOpponent(playerTurn) )
    
    '''
      '@param nodeList - list of Nodes
      '@return list of Nodes that are the parents of the Nodes in nodeList
      '@calling
      '@caller scoreTree
      '''
    def getPriorGen(self, nodeList ):
        parents= []
        for node in nodeList:
            if node.parentNode not in parents:
                parents.append( node.parentNode )
        #parents= set( parents )
        #parents= list( parents )
        return parents
    
    '''
      '@param playerTurn - the player making the analysis
      '@void
      '@spec score all nodes in the tree (self.structure) using weighted-knn values
      '@caller Tree()
      '''
    def scoreTree(self, playerTurn):
        #print "//////////////////////// START SCORE //////////////////////////////"
        for boardNode in self.leafNodes:
            plie= []
            numrows, numColumns= py.shape(boardNode.board)
            for i in range(0,numColumns):
                plie+=  reversed( boardNode.board[0:numrows,i] ) 
            score= knn( 150, self.trainPlies, plie, boardNode.playerTurn )
            boardNode.value= score
        
        #recurse up the tree
        children= self.leafNodes
        parents= self.getPriorGen( children )
        while parents != [None]:
            for parentNode in parents:
                childrenOfParent= self.structure[parentNode]
                player= childrenOfParent[0].playerTurn
                childrenValues= []
                for child in childrenOfParent:
                    childrenValues.append( child.value )
                if player == playerTurn:
                    #get maximum
                    parentNode.value= max( childrenValues )
                else:
                    #get minimum
                    parentNode.value= min( childrenValues )
            children= parents
            parents= self.getPriorGen( children )            

    '''
      '@param playerTurn - the player making the analysis
      '@void
      '@spec score all nodes in the tree (self.structure) using getSequentialCellsPlus
      '@caller Tree()
      '@calling glf.getSequentialCellsPlus, glf.boardContainsWinner
      '''
    def scoreTreeWithSeqCellsPlus( self, playerTurn ):
        opponent= getOpponent( playerTurn )
        for boardNode in self.leafNodes:
            sequentialCells= glf.getSequentialCellsPlus( boardNode.board, 4 )
            myCells= sequentialCells[playerTurn]
            oppCells= sequentialCells[ opponent ]
            winnerFound, winnerPlayerID, _, _=  glf.boardContainsWinner( boardNode.board, 4 )
            if winnerFound and winnerPlayerID == opponent:
                score= len(myCells) - len(oppCells) - 1000.0
            elif winnerFound and winnerPlayerID == playerTurn:
                score= len(myCells) - len(oppCells) + 100.0
            else:
                score= len(myCells) - len(oppCells)           
            boardNode.value= score
           
        #recurse up the tree
        children= self.leafNodes
        parents= self.getPriorGen( children )
        while parents != [None]:
            for parentNode in parents:
                childrenOfParent= self.structure[parentNode]
                player= childrenOfParent[0].playerTurn
                childrenValues= []
                for child in childrenOfParent:
                    childrenValues.append( child.value )
                if player == playerTurn:
                    #get maximum
                    parentNode.value= max( childrenValues )
                else:
                    #get minimum
                    parentNode.value= min( childrenValues )
            children= parents
            parents= self.getPriorGen( children )  
'''
  '@param playerTurn - this player's id
  '@return opposing player's id
  '''
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
 '@caller ai.getLocalMove, other AIs
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

'''
  '@param gameBoard1 - first of two board states to compare
  '@param gameBoard2 - second of two board states to compare
  '@param playerTurn - player making the analysis
  '@spec only flag returned used thus far. Determines which board has a better state for playerTurn
  '@return flag {-1,0,1}, score for playerTurn, score for opponent
  '@calling glf.boardContainsWinner
  '@caller lookAheadOne, lookAheadTwice, lookAheadThrice
  '''
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
  '@param gameBoard - matrix representing game grid's current state
  '@spec score given gameBoard according to a linear combination of the following features:
        2 -- board contains win or loss (consider number of such wins or losses as coefficient)
        2 -- result of scoreBoard (how to use?)
        1 -- the number of offensive plays (from moveYieldsPossibleWin)
        2 -- the number of lose/win opportunities (from sequentialCellsPlus as used in lookAheadTwicePlus)
          --
  '@return value representing linear combination of above features
  '@caller nextMove
  '@calling scoreBoard, moveYieldsPossibleWin, uselessSlotFilter, getValidMoves,
            glf.getSequentialCellsPlus, glf.getSequentialCells, getOpponent
  '''
def evalB2( gameBoard, playerTurn ):
    opponentTurn= getOpponent( playerTurn )
    
    #get whether board contains win or loss (or both)
    allWins= glf.getSequentialCells( gameBoard, 4 )
    wins= len( allWins[playerTurn] )
    losses= len( allWins[opponentTurn] )
    
    #get results of scoreBoard
    myScores, yourScores, candidateSlots= scoreBoard( gameBoard, playerTurn )
    times= 2
    tempPt= 0.0
    tempOt= 0.0
    for score in sorted(candidateSlots.keys(), reverse=True):
        if times == 0:
            break
        nextBests= candidateSlots[score]
        for x,y,player in nextBests:
            if player == playerTurn:
                #update partial score
                tempPt+= score
            else:
                tempOt+= score
        times-=1
    
    #get the number of offensive plays
    offPlays= 0.0
    validMoves= getValidMoves( gameBoard )
    filterWorked, validMoves= uselessSlotFilter( gameBoard, validMoves, playerTurn )
    if filterWorked:
        offPlays= len(validMoves)
        
    #get the number of win/lose opportunities
    sequentialCells= glf.getSequentialCellsPlus( gameBoard, 4 )
    winOpportunities= sequentialCells[playerTurn]
    loseOpportunities= sequentialCells[opponentTurn]
    numWins= len(winOpportunities)
    numLosses= len(loseOpportunities)

    #calculate linear combination
    #value= wins * 10000 + losses * (-10000) + tempPt * 0.3 + tempOt * (-0.1) + offPlays * 0.4 + numWins * 0.3 +  numLosses * (-0.3)
    value= wins * 10000 + losses * (-10000)  + offPlays * 0.4 + numWins * 0.6 + tempPt * 0.1 + numLosses * (-0.1) +  + tempOt * (-0.1)
    print "value is ", value
    return value

'''
  '@param gameBoard - matrix representing game grid's current state
  '@spec score given gameBoard according to a linear combination of the following features:
        2 -- board contains win or loss (consider number of such wins or losses as coefficient)
        2 -- result of scoreBoard (how to use?)
        1 -- the number of offensive plays (from moveYieldsPossibleWin)
        2 -- the number of lose/win opportunities (from sequentialCellsPlus as used in lookAheadTwicePlus)
          --
  '@return value representing linear combination of above features
  '@caller nextMove
  '@calling scoreBoard, moveYieldsPossibleWin, uselessSlotFilter, getValidMoves,
            glf.getSequentialCellsPlus, glf.getSequentialCells, getOpponent
  '''
def evalB( gameBoard, playerTurn ):
    opponentTurn= getOpponent( playerTurn )
    
    #get whether board contains win or loss (or both)
    allWins= glf.getSequentialCellsNoV( gameBoard, 4 )
    wins= len( allWins[playerTurn] )
    losses= len( allWins[opponentTurn] )
    
    #get results of scoreBoard
    myScores, yourScores, candidateSlots= scoreBoard( gameBoard, playerTurn )
    times= 2
    tempPt= 0.0
    tempOt= 0.0
    for score in sorted(candidateSlots.keys(), reverse=True):
        if times == 0:
            break
        nextBests= candidateSlots[score]
        for x,y,player in nextBests:
            if player == playerTurn:
                #update partial score
                tempPt+= score
            else:
                tempOt+= score
        times-=1
    
    #get the number of offensive plays
    offPlays= 0.0
    validMoves= getValidMoves( gameBoard )
    filterWorked, validMoves= uselessSlotFilter( gameBoard, validMoves, playerTurn )
    if filterWorked:
        offPlays= len(validMoves)
        
    #get the number of win/lose opportunities
    sequentialCells= glf.getSequentialCellsPlus( gameBoard, 4 )
    winOpportunities= sequentialCells[playerTurn]
    loseOpportunities= sequentialCells[opponentTurn]
    numWins= len(winOpportunities)
    numLosses= len(loseOpportunities)

    #calculate linear combination
    #value= wins * 10000 + losses * (-10000) + tempPt * 0.3 + tempOt * (-0.1) + offPlays * 0.4 + numWins * 0.3 +  numLosses * (-0.3)
    #value= wins * 10000 + losses * (-10000)  + offPlays * 0.4 + numWins * 0.6 + tempPt * 0.1 + numLosses * (-0.1) +  + tempOt * (-0.1)
    value= wins * 10000 + losses * (-10000)  + offPlays * 0.4 + tempPt * 0.1 + numWins * 0.1 + numLosses * (-0.05) + tempOt * (-0.05)
    print "value is ", value
    return value

  
'''
  '@param startBoard - matrix representing game grid
  '@param results - pointer to list to hold alternate gameBoards 
  '@param playerTurn - player whose turn is being simulated
  '@param numTurns - number of turns to be simulated
  '@spec recursive function to simulate numTurns step starting form 'startBoard' with 'playerTurn'
  '@return void - returns nothing, but uses pointer to 'results' list to return values
  '@caller nextMove
  '@calling getValidMoves
  '''
def simulate(startBoard, results, playerTurn, numTurns, move):
    if numTurns == 0:
        #return startBoard
        results.append( (startBoard, move) )
    else:
        validMoves= getValidMoves( startBoard )
        for (x,y) in validMoves:
            nextBoard= py.copy(startBoard)
            nextBoard[x,y]= playerTurn
            if not move:
                simulate( nextBoard, results, getOpponent(playerTurn), numTurns - 1, (x,y) )
            else:
                simulate( nextBoard, results, getOpponent(playerTurn), numTurns - 1, move )

def gameTree(startBoard, tree, playerTurn, numTurns, move):
    if numTurns == 0:
        #return startBoard
        return startBoard
    else:
        validMoves= getValidMoves( startBoard )
        for (x,y) in validMoves:
            nextBoard= py.copy(startBoard)
            nextBoard[x,y]= playerTurn
            if not move:
                gameTree( nextBoard, results, getOpponent(playerTurn), numTurns - 1, (x,y) )
            else:
                gameTree( nextBoard, results, getOpponent(playerTurn), numTurns - 1, move )


'''
  '@param gameBoard - matrix representing game grid
  '@param lookAheadTimes - number of moves to consider in analysis
  '@param playerTurn - player doing the analysis
  '@return move, final board, and corresponding evalB score based on analysis
  '@calling simulate
  '@caller ai.forwardEval
  '''
def nextMove( gameBoard, lookAheadTimes, playerTurn ):
    finalBoards= []
    simulate( gameBoard, finalBoards, playerTurn, lookAheadTimes, None )
    #now, finalBoards contains a (board, move) pairs.
    #find the best pair based on the eval function
    bestMove= None
    bestBoard= None
    bestValue= -999999999
    ignoreList= []
    for board, move in finalBoards:
        score= evalB( board, playerTurn )
        if score < 0:
            ignoreList.append( move )
    for board, move in finalBoards:
        if move not in ignoreList and  score > bestValue:
            bestMove= move
            bestBoard= board
            bestValue= score
    #print bestMove
    return bestMove, bestBoard, bestValue


        


'''
  '''
def cosineSimilarity( board1, board2 ):
    board1= py.array(board1)
    board2= py.array(board2)
    return py.dot(board1, board2) / ( py.linalg.norm(board1)*py.linalg.norm(board2) )

'''
  '''
def getBestK( k, trainPlies, gameBoard ):
    bestK= [None]*k
    bestVals= [-float('inf')]*k
    #get best k
    for i in range(0,k):
        value= cosineSimilarity( gameBoard, trainPlies[i][0:-1] )
        (minIndex,minVal)= min(enumerate(bestVals), key=itemgetter(1))
        if value > minVal:
            bestVals[minIndex]= value
            bestK[minIndex]= trainPlies[i]   
            
    return bestK, bestVals 

'''
  '@param
  '''
def knn( k, trainPlies, gameBoard, playerTurn ):
    #print gameBoard
    #print gameBoard[0]
    bestK, bestVals= getBestK( k, trainPlies, gameBoard )
    #print "bestKs are: " + str(bestK)
    #weighted majority
    acc= 0.0
    for index in range(0, len(bestVals) ):
        if bestK[index][-1] == 'win':
            acc+= bestVals[index]
        elif bestK[index][-1] == 'loss':
            acc-= bestVals[index]
        elif bestK[index][-1] == 'draw':
            acc+= bestVals[index]
    #print "board is: ", boardNode.board
    #print "value is: ", acc
    return acc
    
    
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
  '@caller functions in ai
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
                    #print" ok"
                    pass
                else:
                    print"this is for opponent"
                    temp= py.copy(futureBoard)
                    temp[slotX,slotY]= opponentTurn
                    isLoss2, winner2, pos2= glf.moveYieldsWin(temp, 4, (slotX,slotY), 'r')
                    #print isLoss2
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
  '@param gameBoard - grid representing game
  '@param isPossibleWin - true if 
  '@calling getOpponent, isPlayable
  '@caller blockSingleLineTrap
  '''
def isSingleLineTrap( gameBoard, isPossibleWin, numPlayerIDs, pos, winningDirection, playerTurn ):
    #print "IN ISSINGLELINETRAP"
    opponentTurn= getOpponent( playerTurn )
    singleLineTraps= [ [0,0, opponentTurn, opponentTurn, 0], [0, opponentTurn, opponentTurn, 0, 0] ]                    
    if not isPossibleWin or numPlayerIDs != 2:
        print "IN ISSINGLELINETRAP --- not valid, so return False"
        return False, None
        #the two != numPlayerIDs must be playable
    targetLine= []
    for row in pos:
        x,y= row
        targetLine.append( gameBoard[x,y] )
    if targetLine not in singleLineTraps:
        print "IN ISSINGLELINETRAP --- not valid, so return False because does not match"
        return False, None
    if targetLine == singleLineTraps[0]:
        #need first, second, and 5th to be playable
        first= pos[0]
        x1,y1= first[0], first[1]
        second= pos[1]
        x2,y2= second[0], second[1]
        fifth= pos[4]
        x5,y5= fifth[0], fifth[1]
        if isPlayable( (x1,y1), gameBoard ) and isPlayable( (x2,y2), gameBoard ) and isPlayable( (x5,y5), gameBoard ):
            return True, (x2,y2)
        else:
            return False, None
    elif targetLine == singleLineTraps[1]:
        #need first, 4th, and 5th to be playable
        first= pos[0]
        x1,y1= first[0], first[1]
        fourth= pos[3]
        x4,y4= fourth[0], fourth[1]
        fifth= pos[4]
        x5,y5= fifth[0], fifth[1]
        if isPlayable( (x1,y1), gameBoard ) and isPlayable( (x4,y4), gameBoard ) and isPlayable( (x5,y5), gameBoard ):
            return True, (x4,y4)
        else:
            return False, None
    else:
        return False, None

'''
  '@param gameBoard - grid representing game
  '@param playerturn - player making the analysis
  '@caller randomOffenseWithTwicePlus, randomOffenseOneWithTwicePlus
  '@calling getOpponent, isSingleLineTrap, moveYieldsPossibleWin
  '''
def blockSingleLineTrap(gameBoard, playerTurn):
    opponentTurn= getOpponent( playerTurn )
    #get new sequentialCells to determine free spaces around this slot
    yourOrScores, myOrScores, orCandidateSlots= scoreBoard(gameBoard, opponentTurn)
    validMoves= getValidMoves(gameBoard)
    for (x,y) in validMoves:
        isPossibleWin, numPlayerIDs, pos, winningDirection= moveYieldsPossibleWin( gameBoard, 5, (x,y), opponentTurn )
        isTrap, blockingMove= isSingleLineTrap( gameBoard, isPossibleWin, numPlayerIDs, pos, winningDirection, playerTurn )
        if isTrap:
            return 1, blockingMove
    return 0, None

'''
  '@param originalBoard
  '@param myMove - my move under consideration
  '@param opponentMove - opponentMove under consideration
  '@param futureBoard - board with myMove and opponentMove playes
  '@param playerTurn - player making the analysis
  '@return flag (1,-1,0) and corresponding move to make (1) or avoid (-1).  0 means no trap detected
  '@caller lookAheadTwicePlus, randomOffenseWithTwicePlus, randomOffenseOneWithTwicePlus
  '@calling getOpponent, glf.getSequentiallCellsPlus
  '@note rough fix to blockTrapFirst by playing near opponent move
  '''
def blockTrap(originalBoard, myMove, opponentMove, futureBoard, playerTurn):
    numrows, numcolumns= py.shape(originalBoard)
    opponentTurn= getOpponent( playerTurn )
    interBoard= py.copy( originalBoard )
    interBoard[myMove]= playerTurn
    winningChains= glf.getSequentialCellsPlus( interBoard, 4 )
    #print "winning Chains: " ,winningChains
    opWins= winningChains[opponentTurn]
    numOpWins= len( opWins )
    
    fwinningChains= glf.getSequentialCellsPlus( futureBoard, 4 )
    fopWins= fwinningChains[opponentTurn]
    print "fopWins: ", fopWins
    fnumOpWins= len( fopWins )
    
    if fnumOpWins >= numOpWins + 2:
        #then there was a trap.
        
        #get entries in fwinningChains that are new (i.e not in winningChains)
        newOpPossibleWins= []
        for pair in fopWins:
            print "pair is: ", pair
            posOfPair, directOfPair= pair
            absent= True
            for pos,direct in opWins:
                if directOfPair == direct and posOfPair.tolist() == pos.tolist():
                    absent= False
            if absent:
                newOpPossibleWins.append(pair)
        #check that there are only 2 new possibilities
        #assert len(newOpPossibleWins) == 2
        
        #go through the first 4
        for posWin in newOpPossibleWins:
            pos,direct= posWin
            rowdirect,columndirect= direct
            for row in pos:
                x,y= row[0], row[1]
                adjRow= x+rowdirect
                adjCol= y+columndirect
                if  adjRow < 6 and adjRow > 0 and adjCol < 7 and adjCol > 0 and isPlayable( (x,y), originalBoard ) and originalBoard[adjRow,adjCol] == opponentTurn:
                    return 1, (x,y)
        return -1, myMove
            
        '''#check if opponentMove is playable from originalBoard
        if isPlayable( opponentMove, originalBoard ):
            return 1, opponentMove
        else:
            #must have been made playable by myMove
            return -1, myMove'''
    else:
        #appears to be no trap
        return 0, myMove

'''
  '@param originalBoard
  '@param myMove - my move under consideration
  '@param opponentMove - opponentMove under consideration
  '@param futureBoard - board with myMove and opponentMove playes
  '@param playerTurn - player making the analysis
  '@return flag (1,-1,0) and corresponding move to make (1) or avoid (-1).  0 means no trap detected
  '@caller lookAheadTwicePlus, randomOffenseWithTwicePlus, randomOffenseOneWithTwicePlus
  '@calling getOpponent, glf.getSequentiallCellsPlus
  '@note problem with placement of move to block trap in single line trap. Tried fixing in blockTrap above
  '''
def blockTrapFirst(originalBoard, myMove, opponentMove, futureBoard, playerTurn):
    opponentTurn= getOpponent( playerTurn )
    interBoard= py.copy( originalBoard )
    interBoard[myMove]= playerTurn
    winningChains= glf.getSequentialCellsPlus( interBoard, 4 )
    opWins= winningChains[opponentTurn]
    numOpWins= len( opWins )
    
    fwinningChains= glf.getSequentialCellsPlus( futureBoard, 4 )
    fopWins= fwinningChains[opponentTurn]
    fnumOpWins= len( fopWins )
    
    if fnumOpWins >= numOpWins + 2:
        #then there was a trap.
        #check if opponentMove is playable from originalBoard
        if isPlayable( opponentMove, originalBoard ):
            return 1, opponentMove
        else:
            #must have been made playable by myMove
            return -1, myMove
    else:
        #appears to be no trap
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
    (numrows, numcolumns)= py.shape(gameBoard)
    for column in range(0, numcolumns):
        for row in range(0, numrows):
            valid= gameBoard[numrows- row- 1,column]
            if valid == 0:
                validMoves= validMoves + [(numrows-row-1, column)]
                break
    return validMoves

'''
  '@param gameBoard - matrix representing game grid
  '@param sequentialPositionsNeeded - number of slots in a chain to consider
  '@param (x,y) - coordinates of target first slot in gameBoard
  '@param playerTurn - player whose turn it is
  '@spec look for sequentialPositionsNeeded of slots filed with 0s or playerTurn's.
         Return the one with the highest numPlayerIDs in their corresponding chain
  '@return solutionFound, bestNumPlayerIDs, bestWinningPositions, bestDirection
           solutionFound - flag for determinging if at least one solution wsa found
           bestNumPlayerIDs - number of playerTurn's filled slots in winning chain
           bestWinningPositions - the coordinates corresponding to the sequentialPositionsNeeded found as solution
           bestDirection - the direction (horizontal or diagonal) in which the sequentialPositionsNeeded slots lie
  '@calling glf.isRangeOutOfBounds
  '@caller uselessSlotFilter
  '''
def moveYieldsPossibleWin( gameBoard, sequentialPositionsNeeded, (x,y), playerTurn  ):
    bestNumPlayerIDs= -1
    bestWinningPositions= py.zeros( ( sequentialPositionsNeeded, 2 ) )
    bestDirection= []

    #directions used for vector manipulations.
    directions= py.array( [ [-1, 1], [0, 1], [1, 1], [1, -1], [0, -1], [-1,-1] ] );


    numrows,numcolumns= py.shape(gameBoard);
    lastMoveRow= x #y;
    lastMoveColumn= y #x;
    playerID= playerTurn;
    solutionFound= False;
    
    #for direct=1:4
    direct= 0;
    while direct < 6:
        numPlayerIDs= 0;
        winningPositions= py.zeros( ( sequentialPositionsNeeded, 2 ) )
        rowdirection= directions[direct,0]
        columndirection= directions[direct, 1]
    #for each possible direction (vertical, horizontal, right and left diagonal), consider the 'sequentialPositionsNeeded' arrangements
    #for p= (-sequentialPositionsNeeded+1):0
        p= -sequentialPositionsNeeded+1
        while p <= 0:
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
                    if numPlayerIDs > bestNumPlayerIDs:
                        bestNumPlayerIDs= numPlayerIDs
                        bestDirection= directions[direct]
                        for resultRow in range( p, (p+sequentialPositionsNeeded) ):
                            bestWinningPositions[resultRow-p, :]= [lastMoveRow + resultRow*rowdirection, lastMoveColumn + resultRow*columndirection]
                    #return solutionFound, numPlayerIDs, winningPositions, directions[direct]
                else:
                        winningPositions= py.zeros( ( sequentialPositionsNeeded, 2 ) )

            p= p + 1;  
        direct= direct + 1
    return solutionFound, bestNumPlayerIDs, bestWinningPositions, bestDirection

'''
  '@param gameBoard - matrix representing game grid
  '@param validMoves - list of coordinates  that are valid moves for the current turn
  '@param playerTurn - current player
  '@return validMoves without slots that cannot contribute to a future win for playerTurn
  '@calling moveYieldsPossibleWin
  '@caller ai.randomOffense, ai.randomOffenseWithTwicePlus
  '''
def uselessSlotFilter(gameBoard, validMoves, playerTurn):
    filteredMoves= []
    for (x,y) in validMoves:
        #get new sequentialCells to determine free spaces around this slot
        isPossibleWin, numPlayerIDs, pos, winningDirection= moveYieldsPossibleWin( gameBoard, 4, (x,y), playerTurn )
        #if x y has at least one chance of turning into a win, add to list.
        if isPossibleWin:
            filteredMoves.append( ( x, y, numPlayerIDs ) )
            
    if len(filteredMoves) == 0:
        #print "uselessSlotFilter --- no good attacking positions"
        return 0, validMoves
    else:
        #print "uselessSlotFilter --- attacking positions: ", filteredMoves
        return 1, filteredMoves
    

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
resp= preventTrapPlus( c2, (3,3), (2,3), c, 2)
resp2= blockTrap( c2, (3,3), (2,3), c, 2 )

d= py.zeros((6,7))
d[5,3]= 1
d[5,2]= 1
d2= py.copy( d )
d2[5,4]= 1
respd= preventTrapPlus( d, (0,0), (5,4), d2, 2 )
respd2= blockTrap( d, (0,0), (5,4), d2, 2 )'''

'''res= []
c= py.zeros((6,7))
#simulate(c, res, 1, 6, None)
move, board, value= nextMove( c, 4, 1 )
print move, board, value'''

#cell= randomMovePlusPlus(b)
#valids= getValidMoves(b)
#res= isBetterState(b,c,1)
