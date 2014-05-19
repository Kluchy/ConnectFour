#GUI API
import matplotlib.pyplot as plt
import numpy
import time
import matplotlib.widgets as mw

NUM_ROWS= 6
NUM_COLUMNS= 7
CIRCLE_RADIUS= 0.5
PLAYER1_COLOR= 'r'
PLAYER2_COLOR= 'b'
moveToProcess= None
playerTurn= PLAYER1_COLOR
boardHandler= None

'''
  '@spec creates and displays the Connect Four Board
  '@return the figure's handler
  '@caller gamelogic.gamePlay
  '''
def createBoard():
    boardHandler= plt.figure()
    ax = boardHandler.gca()
    ax.set_xticks(numpy.arange(0,NUM_COLUMNS+1,1))
    ax.set_yticks(numpy.arange(0,NUM_ROWS+1,1))
    #plt.scatter(x,y)
    plt.grid()
    plt.show()
    return boardHandler#, gameBoard
    
'''
 '@param center - grid cell in which to place circle
 '@param color - color to give circle
 '@return handler for circle
 '@caller gamelogic.gamePlay
 '''
def createCircle( center, color ):
    return plt.Circle(center,CIRCLE_RADIUS,color=color)

'''
  '@param boardHandler - imae handler for game board
  '@param gameBoard - corresponding underlying matrix (not used)
  '@param circle - handler for circle object
  '@spec add circle to board tp reflect player move
  '@caller gamelogic.gamePlay
  '''  
def updateBoard(boardHandler, gameBoard, circle):
    boardHandler.gca().add_artist(circle) 
    return

#not used
def onclick(event):
    global moveToProcess, playerTurn, boardHandler
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)
    #circle= createCircle( (event.xdata,event.ydata), playerTurn )
    #boardHandler.gca().add_artist(circle)
    #boardHandler.draw()
    
     #next player's turn
    if playerTurn == PLAYER1_COLOR:
        playerTurn= PLAYER2_COLOR
    else:
        playerTurn= PLAYER1_COLOR
    
#not used
def getPlayerMove(boardHandler):
    cid = boardHandler.canvas.mpl_connect('button_press_event', onclick)
    return cid

'''plt.ion()
boardHandler= createBoard()
circle= createCircle( (0.5,0.5), PLAYER1_COLOR )
boardHandler.gca().add_artist(circle)
#plt.show()
#time.sleep(2)
circle= createCircle( (1.5,1.5), PLAYER2_COLOR )
boardHandler.gca().add_artist(circle)
#cid= getPlayerMove(boardHandler)
time.sleep(0.5)
#while not moveToProcess:
  # time.sleep(0)
    
#print moveToProcess

#print moveToProcess

v= boardHandler.ginput(n=1, timeout=30)
print v'''