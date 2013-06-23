
import time
import re

def assessBoard(board):
    board = convertBoard(board)
    winners = {"x": False, "o": False, "b": False,"?": False}
    #rows & cols

    
    for i in range(3):
        #rows
        winner = assessRow((board[i][0], board[i][1], board[i][2]))
        winners[winner] = True
        #cols
        winner = assessRow((board[0][i], board[1][i], board[2][i]))
        winners[winner] = True

    #diag 1
    winner = assessRow((board[0][0], board[1][1], board[2][2]))
    winners[winner] = True
    #diag 2
    winner = assessRow((board[2][0], board[1][1], board[0][2]))
    winners[winner] = True

    if winners["b"] or (winners["x"] and winners["o"]):
        return "b"
    elif winners["x"]:
        return "x"
    elif winners["o"]:
        return "o"
    elif winners["?"]:
        return "?"
    else:
        complain("something's gone wrong")

def assessRow(row):
    win = True
    for cell in row:
        if cell != "b":
            win = False
    if win:
        return "b"

    win = True
    for cell in row:
        if cell not in ["x","b"]:
            win = False
    if win:
        return "x"

    win = True
    for cell in row:
        if cell not in ["o","b"]:
            win = False
    if win:
        return "o"
    return "?"

def assessFullBoard(fullBoard,returnCompactBoard = False):

    fullBoard = convertBoard(fullBoard)
    compactBoard = [["?"]*3 for _ in range(3)]
    miniBoard  = [["?"]*3 for _ in range(3)]
    for row in range(3):
        for col in range(3):
            for r in range(3):
                for c in range(3):
                    miniBoard[r][c] = fullBoard[row*3 + r][col*3 + c]
            compactBoard[row][col] = assessBoard(miniBoard)
    return assessBoard(compactBoard)

def convertBoard(board):
    convertedBoard = []
    for row in board:
        convertedRow = []
        for col in row:
            if col in ["?","x","o","b"]:
                convertedRow.append(col)
            elif isinstance(col, int):
                if col%2 == 0:
                    convertedRow.append("x")
                elif col%2 == 1:
                    convertedRow.append("o")
                else:
                    complain("ummmm, what?")
            else:
                complain("invalid board")
        convertedBoard.append(convertedRow)
    return convertedBoard

def boardIsFull(fullBoard, nextToPlayIn):
    row, col = nextToPlayIn
    for r in range(3):
        for c in range(3):
            if fullBoard[row*3 + r][col*3 + c] == "?":
                return False
    return True

def drawBoard(fullBoard,nextToPlayIn = None, printBoard = False):

    fullBoard = convertBoard(fullBoard)
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
    p = re.compile('[012][,][ ]*[012]')
    for attempt in range(10):
        try:
            userIn = raw_input("$: ")
            try:
                if p.match(userIn):
                    UI = (int(userIn[0]),int(userIn[-1]))
                    return UI
                else:
                    print error
            except:
                try:
                    userIn = str(userIn)
                    if userIn == "":
                        userIn = None
                except:
                    userIn = None
        except:
            userIn = None
        if isinstance(userIn, str):
            if userIn.lower() == "kill program":
                main.complain("Got kill request")
            elif userIn.lower() in ["quit", "undo", "q", "u"]:
                return userIn
        print "Either enter a co-ordinate in the form 'r, c' where r and c are integers between 0 and 2, or enter 'quit' to quit, 'undo' to undo the last move or 'kill program' to force the program to crash."






    complain("User failed to enter valid input 10 times.")

            
def playGame( fullBoard = None, nextToPlayIn = None, moveNum = 0,recordGame = True, gameSoFar = []):

    if fullBoard == None:
        fullBoard = [["?"]*9 for _ in range(9)]
        print "All coordinates must be entered in the format:"
        print "$ r, c"
        print "Where r and c are the row and column, indexing from zero."
        print ""
        print ""
        print "New game, please enter the co-ordinates of the first mini-board to be played in:"
        UI = u_in()
        if isinstance(UI, str):
            if UI.lower() in ["u", "undo"]:
                r,c = gameSoFar[-1][0]
                row,col = gameSoFar[-1][1]
                fullBoard[r*3 + row][c*3 + col] = "?"
                gameSoFar.pop()
            elif UI.lower() in ["q", "quit"]:
                return 0
        else:
            row,col = UI
        nextToPlayIn = row, col

    while True:
        if moveNum%2 == 0:
            player = "x"
        else:
            player = "o"
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
            UI = u_in()
            if isinstance(UI, str):
                if UI.lower() in ["u", "undo"]:
                    r,c = gameSoFar[-1][0]
                    row,col = gameSoFar[-1][1]
                    fullBoard[r*3 + row][c*3 + col] = "?"
                    gameSoFar.pop()
                elif UI.lower() in ["q", "quit"]:
                    break
            else:
                row,col = UI
                    
            
                if not boardIsFull(fullBoard,(row,col)):
                    nextToPlayIn = row,col

        else:
            print "It is %s's go. Enter the co-ordinates of your move." % (player,)
            UI = u_in()
            if isinstance(UI, str):
                if UI.lower() in ["u", "undo"]:
                    r,c = gameSoFar[-1][0]
                    row,col = gameSoFar[-1][1]
                    fullBoard[r*3 + row][c*3 + col] = "?"
                    gameSoFar.pop()
                elif UI.lower() in ["q", "quit"]:
                    break
            else:
                row,col = UI
                r = nextToPlayIn[0]*3 + row
                c = nextToPlayIn[1]*3 + col
                if fullBoard[r][c] == "?":
                    fullBoard[r][c] = moveNum
                    gameSoFar.append((nextToPlayIn,(row,col)))
                    moveNum += 1
                    nextToPlayIn = row,col
                    if boardIsFull(fullBoard,(row,col)):
                        nextToPlayIn = None
    if recordGame:
        print gameSoFar
        
    
def playSetGame(gameSequence, continueGame = True,recordContinuedGame = True, printMove = False, delay = 0):
    fullBoard = [["?"]*9 for _ in range(9)]
    nextToPlayIn = None
    moveNum = 0
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
            fullBoard[row][col] = moveNum
            if printMove:
                if moveNum%2 == 0:
                    player = "x"
                else:
                    player = "o"
                print ""
                print ""
                print ""
                print player + " played in mini board " +  str(move[0]) + " in position " + str(move[1])
                drawBoard(fullBoard,move[0],True)
                time.sleep(delay)
            
            moveNum += 1
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
            playGame(fullBoard,nextToPlayIn,moveNum,recordContinuedGame,gameSequence)



                                                                                                            

#Example game, x tries to use three gambits,



playSetGame([
    # First gambit    
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

    # second gambit   
    ((0,1), (0,1)), \
    ((0,1), (0,0)), \
    ((0,0), (0,1)), \
    ((0,1), (2,1)), \
    ((2,1), (0,1)), \
    ((0,1), (2,0)), \
    ((2,0), (0,1)), \
    ((0,1), (1,2)), \
    ((1,2), (0,1)), \
    ((0,1), (0,2)), \
    ((0,2), (0,1)), \
    ((0,1), (2,2)), \
    ((2,2), (0,1)), \
    ((0,1), (1,0)), \

    ((1,0), (0,1)), \
    ((0,1), (1,1)) \




            ],True,True,True,0.1)

"""
    # third gambit    
    ((2,1), (2,1)), \
    ((2,1), (0,0)), \
    ((0,0), (2,1)), \
    ((2,1), (0,2)), \
    ((0,2), (2,1)), \
    ((2,1), (0,1))\
       

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
