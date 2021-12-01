#Dawson chess game solver!

#Max num of columns is mx
mx = 11
sgList = [0,1,1,2]


def mex(future: set):
    for i in range(mx+1):
        if i not in future:
            return i

def xor(a: int, b: int):
    return a^b


def separateByThree(x: int):
    l = []
    x = x-3
    for i in range(1, x):
        l.append((i,x-i))
    return l


def define_SG(x: int):    
    if x>3:
        for i in range(4, x+2):
            future = set()
            future.add(sgList[i-2])
            future.add(sgList[i-3])
            separate = separateByThree(i)

            for j in separate:                
                future.add(xor(sgList[j[0]], sgList[j[1]]))
            sgList.append(mex(future))


def printBoard(board: list, name):
    print("     Board", name)
    print()
    for i in range(len(board[0])):
        print("     ",i+1,end="")
    print()
    print()

    for row in board:
        for cell in row:
            print("     ",cell,end="")
        print()

    print()
    print("----------------------")
    print()
    print()


def findAIFutureMove(boardA: list, boardB: list, boardC: list):

    # Check whether there is a "Must do" move or not
    for col in range(len(boardA[0])):
            if col-1 >= 0:
                if (boardA[0][col] == "B") and (boardA[1][col-1] == "W"):
                    return ("boardA", col, "type0", col-1)
            if col+1 < len(boardA[0]):
                if (boardA[0][col] == "B") and (boardA[1][col+1] == "W"):
                    return ("boardA", col, "type0", col+1)
    
    for col in range(len(boardB[0])):
            if col-1 >= 0:
                if (boardB[0][col] == "B") and (boardB[1][col-1] == "W"):
                    return ("boardB", col, "type0", col-1)
            if col+1 < len(boardB[0]):
                if (boardB[0][col] == "B") and (boardB[1][col+1] == "W"):
                    return ("boardB", col, "type0", col+1)
    for col in range(len(boardC[0])):
            if col-1 >= 0:
                if (boardC[0][col] == "B") and (boardC[1][col-1] == "W"):
                    return ("boardC", col, "type0", col-1)
            if col+1 < len(boardC[0]):
                if (boardC[0][col] == "B") and (boardC[1][col+1] == "W"):
                    return ("boardC", col, "type0", col+1)

    # Calculating the boards SG (total SG of the game)
    partsA = []
    tmpPartSize = 0
    for col in range(len(boardA[0])):
        if (boardA[0][col]=="B" and boardA[2][col]=="W"):
            tmpPartSize += 1
        else:
            if tmpPartSize != 0:
                partsA.append((tmpPartSize, sgList[tmpPartSize]))
                tmpPartSize = 0
    if tmpPartSize != 0:
        partsA.append((tmpPartSize, sgList[tmpPartSize]))
        tmpPartSize = 0

    partsB = []
    tmpPartSize = 0
    for col in range(len(boardB[0])):
        if (boardB[0][col]=="B" and boardB[2][col]=="W"):
            tmpPartSize += 1
        else:
            if tmpPartSize != 0:
                partsB.append((tmpPartSize, sgList[tmpPartSize]))
                tmpPartSize = 0
    if tmpPartSize != 0:
        partsB.append((tmpPartSize, sgList[tmpPartSize]))
        tmpPartSize = 0

    partsC = []
    tmpPartSize = 0
    for col in range(len(boardC[0])):
        if (boardC[0][col]=="B" and boardC[2][col]=="W"):
            tmpPartSize += 1
        else:
            if tmpPartSize != 0:
                partsC.append((tmpPartSize, sgList[tmpPartSize]))
                tmpPartSize = 0
    if tmpPartSize != 0:
        partsC.append((tmpPartSize, sgList[tmpPartSize]))
        tmpPartSize = 0
    
    sgA = 0
    for prt in partsA:
        sgA = xor(sgA, prt[1])
    # print("sgA", sgA)
    sgB = 0
    for prt in partsB:
        sgB = xor(sgB, prt[1])
    # print("sgB", sgB)
    sgC = 0
    for prt in partsC:
        sgC = xor(sgC, prt[1])
    # print("sgC", sgC)
    
    totalSG = xor(sgA, sgB)
    totalSG = xor(totalSG, sgC)
    # print("TOT", totalSG)

    # print("partsA" , partsA)
    # print("partsB" , partsB)
    # print("partsC" , partsC)

    if totalSG > 0:
        #check which table makes totalSG = 0
        
        numPrevCol = 0
        for prt in range(len(partsA)):
            tmp_sgA = sgA
            tmp_sgA = xor(tmp_sgA, partsA[prt][1])
            atotalSG = xor(sgB, sgC)
            if (partsA[prt][0] > 1) and (xor(xor(sgList[partsA[prt][0]-2],tmp_sgA),atotalSG) == 0):

                return ("boardA", numPrevCol, "type1", -1)
            elif  (partsA[prt][0] > 2) and (xor(xor(sgList[partsA[prt][0]-3],tmp_sgA), atotalSG) == 0):
                return ("boardA", numPrevCol, "type2", -1)
            elif (partsA[prt][0] > 4):
                for i in range(1, partsA[prt][0]-3):
                    newprt = xor(i, sgList[partsA[prt][0]-3-i])
                    if xor(xor(tmp_sgA, newprt),atotalSG) == 0:
                        return ("boardA", numPrevCol, "type3", i)
            elif (partsA[prt][0] == 1) and (xor(xor(sgList[partsA[prt][0]-1],tmp_sgA), atotalSG) == 0):
                return ("boardA", numPrevCol, "type5", -1)
            numPrevCol += partsA[prt][0]

        numPrevCol = 0
        for prt in range(len(partsB)):
            tmp_sgB = sgB
            tmp_sgB = xor(tmp_sgB, partsB[prt][1])
            btotalSG = xor(sgA, sgC)
            if (partsB[prt][0] > 1) and (xor(xor(sgList[partsB[prt][0]-2],tmp_sgB), btotalSG) == 0):
                return ("boardB", numPrevCol, "type1", -1)
            elif  (partsB[prt][0] > 2) and(xor(xor(sgList[partsB[prt][0]-3],tmp_sgB), btotalSG) == 0):
                return ("boardB", numPrevCol, "type2", -1)
            elif (partsB[prt][0] > 4):
                for i in range(1, partsB[prt][0]-3):
                    newprt = xor(i, sgList[partsB[prt][0]-3-i])
                    if xor(xor(tmp_sgB, newprt),btotalSG) == 0:
                        return ("boardB", numPrevCol, "type3", i)
            elif (partsB[prt][0] == 1) and (xor(xor(sgList[partsB[prt][0]-1],tmp_sgB), btotalSG) == 0):
                return ("boardB", numPrevCol, "type5", -1)
            numPrevCol += partsB[prt][0]

        numPrevCol = 0
        for prt in range(len(partsC)):
            tmp_sgC = sgC
            tmp_sgC = xor(tmp_sgC, partsC[prt][1])
            ctotalSG = xor(sgB, sgA)
            if (partsC[prt][0] > 1) and (xor(xor(sgList[partsC[prt][0]-2],tmp_sgC), ctotalSG) == 0):
                return ("boardC", numPrevCol, "type1", -1)
            elif  (partsC[prt][0] > 2) and(xor(xor(sgList[partsC[prt][0]-3],tmp_sgC), ctotalSG) == 0):
                return ("boardC", numPrevCol, "type2", -1)
            elif (partsC[prt][0] > 4):
                for i in range(1, partsC[prt][0]-3):
                    newprt = xor(i, sgList[partsC[prt][0]-3-i])
                    if xor(xor(tmp_sgC, newprt), ctotalSG) == 0:
                        return ("boardC", numPrevCol, "type3", i)
            elif (partsC[prt][0] == 1) and (xor(xor(sgList[partsC[prt][0]-1],tmp_sgC), ctotalSG) == 0):
                return ("boardC", numPrevCol, "type5", -1)
            numPrevCol += partsC[prt][0]

    elif totalSG == 0:
        for col in range(len(boardA[0])):
            if (boardA[0][col] == "B") and (boardA[1][col] == "."):
                return ("boardA", col, "type4", -1)
        
        for col in range(len(boardB[0])):
            if (boardB[0][col] == "B") and (boardB[1][col] == "."):
                return ("boardB", col, "type4", -1)
        
        for col in range(len(boardC[0])):
            if (boardC[0][col] == "B") and (boardC[1][col] == "."):
                return ("boardC", col, "type4", -1)


def doAIFutureMove(futureMove: tuple, boardA: list, boardB: list, boardC: list):
    
    if futureMove[2] == "type0":

        if futureMove[0] == "boardA":
            boardA[1][futureMove[3]] = "B"
            boardA[0][futureMove[1]] = "."
        elif futureMove[0] == "boardB":
            boardB[1][futureMove[3]] = "B"
            boardB[0][futureMove[1]] = "."
        elif futureMove[0] == "boardC":
            boardC[1][futureMove[3]] = "B"
            boardC[0][futureMove[1]] = "."
    
    elif (futureMove[2] == "type1") or (futureMove[2] == "type2") or (futureMove[2] == "type3") or (futureMove[2] == "type5"):
        if futureMove[0] == "boardA":
            passedCol = 0
            for col in range(len(boardA[0])):
                if (boardA[0][col]=="B" and boardA[2][col]=="W") and (passedCol == futureMove[1]):
                    if (futureMove[2] == "type1") or (futureMove[2] == "type5"):
                        boardA[1][col] = "B"
                        boardA[0][col] = "."
                        return
                    elif futureMove[2] == "type2":
                        boardA[1][col+1] = "B"
                        boardA[0][col+1] = "."
                        return
                    elif futureMove[2] == "type3":
                        boardA[1][col+futureMove[3]+1] = "B"
                        boardA[0][col+futureMove[3]+1] = "."
                        return

                elif (boardA[0][col]=="B") and (boardA[2][col]=="W"):
                    passedCol += 1

        elif futureMove[0] == "boardB":
            passedCol = 0
            for col in range(len(boardB[0])):
                if (boardB[0][col]=="B" and boardB[2][col]=="W") and (passedCol == futureMove[1]):
                    if (futureMove[2] == "type1") or (futureMove[2] == "type5"):
                        boardB[1][col] = "B"
                        boardB[0][col] = "."
                        return
                    elif futureMove[2] == "type2":
                        boardB[1][col+1] = "B"
                        boardB[0][col+1] = "."
                        return
                    elif futureMove[2] == "type3":
                        boardB[1][col+futureMove[3]+1] = "B"
                        boardB[0][col+futureMove[3]+1] = "."
                        return                    
    
                elif (boardB[0][col]=="B") and (boardB[2][col]=="W"):
                    passedCol += 1
        
        elif futureMove[0] == "boardC":
            passedCol = 0
            for col in range(len(boardC[0])):
                if (boardC[0][col]=="B" and boardC[2][col]=="W") and (passedCol == futureMove[1]):
                    if (futureMove[2] == "type1") or (futureMove[2] == "type5"):
                        boardC[1][col] = "B"
                        boardC[0][col] = "."
                        return
                    elif futureMove[2] == "type2":
                        boardC[1][col+1] = "B"
                        boardC[0][col+1] = "."
                        return
                    elif futureMove[2] == "type3":
                        boardC[1][col+futureMove[3]+1] = "B"
                        boardC[0][col+futureMove[3]+1] = "."
                        return                
    
                elif (boardC[0][col]=="B") and (boardC[2][col]=="W"):
                    passedCol += 1  

    elif futureMove[2] == "type4":
        col = futureMove[1]

        if futureMove[0] == "boardA":                
            boardA[1][col] = "B"
            boardA[0][col] = "."
            return

        elif futureMove[0] == "boardB":        
            boardB[1][col] = "B"
            boardB[0][col] = "."
            return
    
        
        elif futureMove[0] == "boardC":            
            boardC[1][col] = "B"
            boardC[0][col] = "."
            return

    

def doHumanFutureMove(board: list, player, srcColumn, destColumn):
    # check the move?
    if player=="W":
        board[1][destColumn] = "W"
        board[2][srcColumn] = "."
    else:
        board[1][destColumn] = "B"
        board[0][srcColumn] = "."


def checkWinning(boardA: list, boardB: list, boardC: list, player):
    opponent = "W" if player=="B" else "B"
    
    if opponent=="W":
        for cell in range(len(boardA[2])):
            if boardA[2][cell] == "W" and boardA[1][cell]==".":
                return False
            if cell - 1 >= 0:
                if boardA[2][cell] == "W" and boardA[1][cell-1]=="B":
                    return False
            if cell + 1 < len(boardA[0]):
                if boardA[2][cell] == "W" and boardA[1][cell+1]=="B":
                    return False
        for cell in range(len(boardB[2])):
            if boardB[2][cell] == "W" and boardB[1][cell]==".":
                return False
            if cell - 1 >= 0:
                if boardB[2][cell] == "W" and boardB[1][cell-1]=="B":
                    return False
            if cell + 1 < len(boardA[0]):
                if boardB[2][cell] == "W" and boardB[1][cell+1]=="B":
                    return False
        for cell in range(len(boardC[2])):
            if boardC[2][cell] == "W" and boardC[1][cell]==".":
                return False
            if cell - 1 >= 0:
                if boardC[2][cell] == "W" and boardC[1][cell-1]=="B":
                    return False
            if cell + 1 < len(boardC[0]):
                if boardC[2][cell] == "W" and boardC[1][cell+1]=="B":
                    return False
        return True
    
    elif opponent=="B":
        for cell in range(len(boardA[2])):
            if boardA[0][cell] == "B" and boardA[1][cell]==".":
                return False
            if cell - 1 >= 0:
                if boardA[0][cell] == "B" and boardA[1][cell-1]=="W":
                    return False
            if cell + 1 < len(boardA[0]):
                if boardA[0][cell] == "B" and boardA[1][cell+1]=="W":
                    return False
        for cell in range(len(boardB[2])):
            if boardB[0][cell] == "B" and boardB[1][cell]==".":
                return False
            if cell - 1 >= 0:
                if boardB[0][cell] == "B" and boardB[1][cell-1]=="W":
                    return False
            if cell + 1 < len(boardB[0]):
                if boardB[0][cell] == "B" and boardB[1][cell+1]=="W":
                    return False
        for cell in range(len(boardC[2])):
            if boardC[0][cell] == "B" and boardC[1][cell]==".":
                return False
            if cell - 1 >= 0:
                if boardC[0][cell] == "B" and boardC[1][cell-1]=="W":
                    return False
            if cell + 1 < len(boardC[0]):
                if boardC[0][cell] == "B" and boardC[1][cell+1]=="W":
                    return False
        return True

#-----------------------------------------------------------------------------------------------------------    

#staring page
print()
print("                                                         Welcome to Dawson Chess Game!")
print("                                       ------------------------------------------------------------------")
# print()
print()
print("     If you want to play vs another human enter 'H' else enter 'C': ", end="")

gameMode = input()

# we have three game x cols and y cols and 18-x-y cols
print("     input the code(!) : ",end="")
inp = int(input())

#Init parametrs
x = inp % 10    
y = inp % 100
y = y // 10
player = "W"
running = False
define_SG(mx)
# print(sgList)

#creating the boards
#board A:
boardA = []

row = []
for i in range (x):
    row.append("B")
boardA.append(row)
row = []
for i in range (x):
    row.append(".")
boardA.append(row)
row = []
for i in range (x):
    row.append("W")
boardA.append(row)
#board B:
boardB = []

row = []
for i in range (y):
    row.append("B")
boardB.append(row)
row = []
for i in range (y):
    row.append(".")
boardB.append(row)
row = []
for i in range (y):
    row.append("W")
boardB.append(row)
#board C:
boardC = []

row = []
for i in range (mx-x-y):
    row.append("B")
boardC.append(row)
row = []
for i in range (mx-x-y):
    row.append(".")
boardC.append(row)
row = []
for i in range (mx-x-y):
    row.append("W")
boardC.append(row)        
print("     We'll have three games with ", x,",", y, "and", mx-x-y, "columns.")
print()
print()    

if gameMode == 'H' or gameMode == 'h':
    # START
    running = True
    while running:
        
        printBoard(boardA, "A")
        printBoard(boardB, "B")
        printBoard(boardC, "C")
        print("     It's",player,"turn. Choose the board you want: ",end="")
        board = input()
        print("     Choose the src column you want: ",end="")
        srcColumn = int(input())
        srcColumn = srcColumn - 1
        print("     Choose the dest column you want: ",end="")
        destColumn = int(input())
        destColumn = destColumn - 1
        
        if board=="a" or board=="A":
            doHumanFutureMove(boardA,player,srcColumn,destColumn)
        elif board=="b" or board=="B":
            doHumanFutureMove(boardB,player,srcColumn,destColumn)
        elif board=="c" or board=="C":
            doHumanFutureMove(boardC,player,srcColumn,destColumn)
        
        if checkWinning(boardA, boardB, boardC,player):             
            printBoard(boardA, "A")
            printBoard(boardB, "B")
            printBoard(boardC, "C")
            print("     Player", player, "Won!")
            print()
            print("     See U Soon :)")
            running = False
        player = "W" if player=="B" else "B"               
            
        print()
        print()
        print()
        

elif gameMode == 'C' or gameMode == 'c':

    # START
    printBoard(boardA, "A")
    printBoard(boardB, "B")
    printBoard(boardC, "C")
    running = True

    while running:

        print("     It's",player,"turn. Choose the board you want: ",end="")
        board = input()
        print("     Choose the src column you want: ",end="")
        srcColumn = int(input())
        srcColumn = srcColumn - 1
        print("     Choose the dest column you want: ",end="")
        destColumn = int(input())
        destColumn = destColumn - 1
        
        if board=="a" or board=="A":
            doHumanFutureMove(boardA,player,srcColumn,destColumn)
        elif board=="b" or board=="B":
            doHumanFutureMove(boardB,player,srcColumn,destColumn)
        elif board=="c" or board=="C":
            doHumanFutureMove(boardC,player,srcColumn,destColumn)
                
        
        if checkWinning(boardA, boardB, boardC,"W"):
            printBoard(boardA, "A")
            printBoard(boardB, "B")
            printBoard(boardC, "C")
            print("     Player", "W", "Won!")
            print()
            print("     See U Soon :)")
            running = False

        AIfutureMove = findAIFutureMove(boardA, boardB, boardC)
        # print("AIfutureMove IS ", AIfutureMove)
        doAIFutureMove(AIfutureMove, boardA, boardB, boardC)


        printBoard(boardA, "A")
        printBoard(boardB, "B")
        printBoard(boardC, "C")
        print("     Player B moved the action in ", AIfutureMove[0])


        if checkWinning(boardA, boardB, boardC,"B"):
            printBoard(boardA, "A")
            printBoard(boardB, "B")
            printBoard(boardC, "C")
            print("     Player", "B", "Won!")
            print()
            print("     See U Soon :)")
            running = False                              
            
        print()
        print()        