
import time

def assessBoard(board):

    #rows & cols
    for i in range(3):
        #rows
        if board[i][0] != "?":
            if board[i][1] == board[i][0] and board[i][1] == board[i][2]:
                return board[i][0]
        #cols
        if board[0][i] != "?":
            if board[1][i] == board[0][i] and board[1][i] == board[2][i]:
                return board[0][i]
    #diag 1
    if board[0][0] != "?":
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
    #diag 2
    if board[0][2] != "?":
        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
             return board[0][2]
    return "?"


def assessFullBoard(fullBoard,returnCompactBoard = False):
    compactBoard = [["?"]*3 for _ in range(3)]
    miniBoard  = [["?"]*3 for _ in range(3)]
    for row in range(3):
        for col in range(3):
            for r in range(3):
                for c in range(3):
                    miniBoard[r][c] = fullBoard[row*3 + r][col*3 + c]
            compactBoard[row][col] = assessBoard(miniBoard)
    return assessBoard(compactBoard)

def boardIsFull(fullBoard, nextToPlayIn):
    row, col = nextToPlayIn
    for r in range(3):
        for c in range(3):
            if fullBoard[row*3 + r][col*3 + c] == "?":
                return False
    return True

def drawBoard(fullBoard,nextToPlayIn = None, printBoard = False):

    boardMatrix = [[" "]*25 for _ in range(16)]

    # Draw in board outline

    for row in [0,5,10,15]:
        for col in range(len(boardMatrix[row])):
            boardMatrix[row][col] = "_"
        for col in [0,8,16,24]:
            boardMatrix[row][col] = " "

    for col in [0,8,16,24]:
        for row in range(1,len(boardMatrix)):
            boardMatrix[row][col] = "|"



    # Draw in mini boards
    rowTable = [2,3,4,7,8,9,12,13,14]
    colTable = [2,4,6,10,12,14,18,20,22]
    for row in range(9):
        for col in range(9):
            boardMatrix[rowTable[row]][colTable[col]] = fullBoard[row][col]
    

    # Highlight miniboard that's about to be played in
    if nextToPlayIn != None:
        r_jump = nextToPlayIn[0] * 5
        c_jump = nextToPlayIn[1] * 8

        # Top/bottom sides
        for row in [r_jump,r_jump + 5]:
            for col in [c_jump + 2, c_jump + 4, c_jump + 6]:
                boardMatrix[row][col] = " "
        

        # Left/right sides
        for row in [r_jump +2,r_jump + 4]:
            for col in [c_jump, c_jump + 8]:
                boardMatrix[row][col] = " "

        
    drawnBoard = []
    for row in boardMatrix:
        newRow = ""
        for col in row:
            newRow = newRow + col
        drawnBoard.append(newRow)
    



    if printBoard:
        for row in drawnBoard:
            print row




def u_in():
    for attempt in range(10):
        try:
            if attempt == 9:
                print "Last try!"
            userIn = input("$ ")
            try:
                r,c = userIn
                if r in [0,1,2] and c in [0,1,2]:
                    return userIn
            except:
               pass 
        except:
            userIn = None
    complain("User failed to enter valid input 10 times.")

            
def playGame( fullBoard = None, nextToPlayIn = None, player = "x",recordGame = False, gameSoFar = []):

    if fullBoard == None:
        fullBoard = [["?"]*9 for _ in range(9)]
        print '\n' * 50
        print "All coordinates must be entered in the format:"
        print "$ r, c"
        print "Where r and c are the row and column, indexing from zero."
        print ""
        print ""
        print "New game, please enter the co-ordinates of the first mini-board to be played in:"
        row,col = u_in()
        nextToPlayIn = row, col

    while True:
        winner = assessFullBoard(fullBoard)


        print "The winner is '%s'" % (winner,)

        drawBoard(fullBoard,nextToPlayIn, True)
        
        if winner != "?":
            break
        
        if nextToPlayIn == None:
            anySpaceLeft = False
            for row in range(3):
                for col in range(3):
                    if not boardIsFull(fullBoard,(row,col)):
                        anySpaceLeft = True
            if anySpaceLeft == False:
                break
                        
                    
            print "It is %s's go. No mini-board has been specified, please enter the co-ordinates of the first mini-board to be played in:" % (player,)
            row,col = u_in()
            
            if not boardIsFull(fullBoard,(row,col)):
                nextToPlayIn = row,col

        else:
            print "It is %s's go. Enter the co-ordinates of your move." % (player,)
            row,col = u_in()
            r = nextToPlayIn[0]*3 + row]
            c = nextToPlayIn[1]*3 + col]
            if fullBoard[r][c] == "?":
                fullBoard[r][c] = player

                if recordGame:
                    gameSoFar.append((nextToPlayIn,(row,col)))
                if player == "x":
                    player = "o"
                else:
                    player = "x"
                nextToPlayIn = row,col
        
    
def playSetGame(gameSequence, continueGame = True,recordContinuedGame = False, printMove = False, delay = 0):
    fullBoard = [["?"]*9 for _ in range(9)]
    nextToPlayIn = None
    player = "x"
    for move in gameSequence:
        if assessFullBoard(fullBoard) != "?":
            print assessFullBoard(fullBoard) + " has already won! Cutting game sequence short."
            break
        if nextToPlayIn == None:
            nextToPlayIn = move[0]
        if nextToPlayIn != move[0]:
            complain("Must play in the mini-board designated.")
        row, col = move[0][0]*3 + move[1][0], move[0][1]*3 + move[1][1]

        if fullBoard[row][col] == "?":
            fullBoard[row][col] = player
            if printMove:
                print ""
                print ""
                print ""
                print player + " played in mini board " +  str(move[0]) + " in position " + str(move[1])
                drawBoard(fullBoard,move[0],True)
                time.sleep(delay)
            
            if player == "x":
                player = "o"
            else:
                player = "x"

            nextToPlayIn = move[1]
            if boardIsFull(fullBoard, nextToPlayIn):
                nextToPlayIn = None
        
        
                
        else:
            complain("Must play in an empty square.")

    if continueGame:
        if assessFullBoard(fullBoard) != "?":
            print assessFullBoard(fullBoard) + " has won! Not continuing game"
        else:
            print ""
            print ""
            print ""
            print ""
            playGame(fullBoard,nextToPlayIn,player,recordContinuedGame,gameSequence)




playSetGame([
    ((1,1), (1,1)), \
    ((1,1), (0,0)), \
    ((0,0), (1,1)), \
    ((1,1), (1,0)), \
    ((1,0), (1,1)), \
    ((1,1), (2,0)), \
    ((2,0), (1,1)), \
    ((1,1), (0,2)), \
    ((0,2), (1,1)), \
    ((1,1), (2,2)), \
    ((2,2), (1,1)), \
    ((1,1), (2,1)), \
    ((2,1), (1,1)), \
    ((1,1), (1,2)), \
    ((1,2), (1,1)), \
    ((1,1), (0,1)), \
    ((0,1), (0,1)), \
    ((0,1), (1,1))\
       


            ],True,True,True,1)
"""
 x to play.

 _______ _______ ____
|       |       |   
| ? x ? | ? ? ? |
| ? x ? | ? x o |
| ? x ? | ? ? ? |
|_______|_ _ _ _|
|       |
| 
|       |


Enter the co-ordinate of your move (in the form x,y).
$:
"""
