#Algorithm to solve ZERO-SUM matrix in game theory
#Matrix dimensions should be less than 100

from copy import deepcopy

#Finding LOLA
def findLOLA(mtrx :list, r, c):

    lolaCul = -1
    lolaRow = -1
    lolaFindFlag = False
    lola = -1

    for a in range(1, len(mtrx[r-1])-1):
        if mtrx[r-1][a] < 0 :
            lolaCul = a
            lolaFindFlag = True
            break
    if lolaFindFlag :
        tempMin = 20000000
        for rr in range(1, len(mtrx)-1):
            if(mtrx[rr][lolaCul]>0):
                if float((mtrx[rr][c-1]) / (mtrx[rr][lolaCul])) < tempMin:
                    tempMin = float((mtrx[rr][c-1]) / (mtrx[rr][lolaCul]))
                    lolaRow = rr
                    lola = mtrx[lolaRow][lolaCul]
        if tempMin != 20000000:
            return(lola, lolaRow, lolaCul)
        else:
            return(-1,-1,-1)

    else:
        return(-1,-1,-1)

#----------------------------------------------

# Creating the matrix

mtrx = []
tmtrx = []
mn = 0
print("Enter your matrix.")
row = str(input())
while row != "solve!":
    r = list(map(float, row.split(" ")))
    # to find the min element
    mnr = min(r)
    if mnr<mn:
        mn = mnr    
    tmtrx.append(r)    
    row = str(input())

# to make sure the value is positive
if mn < 0:
    mn = (-1)*mn

for r in tmtrx:
    newR = [x+mn for x in r]
    mtrx.append(newR)


# column of 1 in the end
for row in mtrx:
    row.append(1.0)

#row of -1 in the other end!
row = [0]
for _ in range(len(mtrx[0])-1):
    row.append(-1.0)
row.append(0.0)
mtrx.append(row)

#sign for Xs
for i in range(len(mtrx)-1):
    mtrx[i].insert(0,100*(i+1))

#sign for Ys
numbers = []
for i in range(len(mtrx[0])-1):
    numbers.append(i)
mtrx.insert(0,numbers)

c = len(mtrx[0])+1
r = len(mtrx)

#----------------------------------------------

#the Algorithm Part
theLOLA, theR, theC = findLOLA(mtrx, r, c)

while((theLOLA, theR, theC) != (-1, -1, -1)):  
    
    tmpmtrx = deepcopy(mtrx)
    
    #Update the LOLA column
    for i in range(1, r):
        if i != theR:
            tmpmtrx[i][theC] = - float(mtrx[i][theC] / theLOLA)
    
    #Update the LOLA row
    for j in range(1, c):
        if j != theC:
            tmpmtrx[theR][j] = float(mtrx[theR][j] / theLOLA)
    
    #Update the rest
    for i in range(1, r):
        for j in range(1, c):
            if i != theR and j!= theC:
                tmpmtrx[i][j] = mtrx[i][j] - float((mtrx[theR][j])*(mtrx[i][theC])/(theLOLA))
    
    #Update the LOLA
    tmpmtrx[theR][theC] = float(1/theLOLA)

    #Update the LOLA x and y
    tmp = tmpmtrx[0][theC]
    tmpmtrx[0][theC] = tmpmtrx[theR][0]
    tmpmtrx[theR][0] = tmp
    
    mtrx = []
    for i in tmpmtrx:
        mtrx.append(i)
    theLOLA, theR, theC = findLOLA(mtrx, r, c)
   
print()
print("The value of matrix is", format(float(1/mtrx[r-1][c-1])-mn, ".2f"))

#caculating the P
P = [0 for i in range(len(mtrx[0]))]
for j in range(1, len(mtrx[0])):
    if mtrx[0][j]>99:
        P[mtrx[0][j]//100] = float(mtrx[r-1][j] / mtrx[r-1][c-1])

#caculating the Q
Q = [0 for j in range(1, len(mtrx))]
for i in range(1, len(mtrx)-1):
    if mtrx[i][0]<100:
        Q[mtrx[i][0]] = float(mtrx[i][c-1] / mtrx[r-1][c-1])


#PRINTING THE P AND Q
print("The strategy for 1st player is: ( ", end="")
for i in range(1, len(P)-1):
    print(format(P[i],".2f"),", ",end="")

print(format(P[len(P)-1],".2f"), ")")

print("The strategy for 2nd player is: ( ",end="")
for i in range(1, len(Q)-1):
    print(format(Q[i],".2f"),", ",end="")

print(format(Q[len(Q)-1],".2f"), ")")