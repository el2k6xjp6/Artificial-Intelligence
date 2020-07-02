from random import shuffle
from os.path import exists

class Agent:
    def __init__(self,board):
        self.LoadBoard(board)

    def LoadBoard(self,file,board=[],Bboard=[],Rboard=[]):
        with open(file,"r") as reader:
            self.dimension=int(reader.readline().strip())
            for i in range(self.dimension):
                row=reader.readline().split()
                board.append(row)
                for j in range(self.dimension):
                    if row[j]=="B":
                        Bboard.append([i,j])
                    elif row[j]=="R":
                        Rboard.append([i,j])
        self.board=board
        self.mboard={"B":Bboard,"R":Rboard}
        print(self.dimension)
        for r in self.board:
            print(' '.join(r))

    def BFS(self,limit,i,j):
        done=[]
        found=[[i,j]]
        good=0
        bad=0
        for i in range(limit):
            for node in [i for i in found]:
                if node[0]>0:
                    if self.board[node[0]-1][node[1]]!="X":
                        if (not([node[0]-1,node[1]] in found) and not([node[0]-1,node[1]] in done)):
                            if self.IsSideEffect(node[0]-1,node[1]):
                                if self.board[node[0]-1][node[1]]==self.color[1]:
                                    good+=1
                                elif self.board[node[0]-1][node[1]]==self.color[0]:
                                    bad+=1
                            found.append([node[0]-1,node[1]])
                if node[0]<self.dimension-1:
                    if self.board[node[0]+1][node[1]]!="X":
                        if (not([node[0]+1,node[1]] in found) and not([node[0]+1,node[1]] in done)):
                            if self.IsSideEffect(node[0]+1,node[1]):
                                if self.board[node[0]+1][node[1]]==self.color[1]:
                                    good+=1
                                elif self.board[node[0]+1][node[1]]==self.color[0]:
                                    bad+=1
                            found.append([node[0]+1,node[1]])
                if node[1]>0:
                    if self.board[node[0]][node[1]-1]!="X":
                        if (not([node[0],node[1]-1] in found) and not([node[0],node[1]-1] in done)):
                            if self.IsSideEffect(node[0],node[1]-1):
                                if self.board[node[0]][node[1]-1]==self.color[1]:
                                    good+=1
                                elif self.board[node[0]][node[1]-1]==self.color[0]:
                                    bad+=1
                            found.append([node[0],node[1]-1])
                if node[1]<self.dimension-1:
                    if self.board[node[0]][node[1]+1]!="X":
                        if (not([node[0],node[1]+1] in found) and not([node[0],node[1]+1] in done)):
                            if self.IsSideEffect(node[0],node[1]+1):
                                if self.board[node[0]][node[1]+1]==self.color[1]:
                                    good+=1
                                elif self.board[node[0]][node[1]+1]==self.color[0]:
                                    bad+=1
                            found.append([node[0],node[1]+1])
                found.remove(node)
                done.append(node)
        return good,bad

    def DecideNextMove(self):
        candidate=[index for index in self.mboard[self.color[1]]]
        best=[]
        for i in range(2*self.dimension-2):
            good,bad=0,self.dimension**2
            for index in [i for i in candidate]:
                g,b=self.BFS(i,index[0],index[1])
                if b<bad:
                    best=[]
                    best.append(index)
                    bad=b
                elif b==bad:
                    best.append(index)
            if len(best)==1:
                return best[0][0],best[0][1]
            candidate=best
        shuffle(best)
        return candidate[0][0],candidate[0][1]

    def IsSideEffect(self,i,j):
        if i>0 :
            if self.board[i-1][j]=="X":
                return True
        if i<self.dimension-1:
            if self.board[i+1][j]=="X":
                return True
        if j>0:
            if self.board[i][j-1]=="X":
                return True
        if j<self.dimension-1:
            if self.board[i][j+1]=="X":
                return True
        return False

    def SideEffect(self,i,j):
        if i>0 :
            if self.board[i-1][j]!="X":
                if self.IsSideEffect(i-1,j):
                    self.mboard[self.board[i-1][j]].remove([i-1,j])
                    self.board[i-1][j]="X"
                    # print("Side effect {} {}".format(i-1,j))
        if i<self.dimension-1:
            if self.board[i+1][j]!="X":
                if self.IsSideEffect(i+1,j):
                    self.mboard[self.board[i+1][j]].remove([i+1,j])
                    self.board[i+1][j]="X"
                    # print("Side effect {} {}".format(i+1,j))
        if j>0:
            if self.board[i][j-1]!="X":
                if self.IsSideEffect(i,j-1):
                    self.mboard[self.board[i][j-1]].remove([i,j-1])
                    self.board[i][j-1]="X"
                    # print("Side effect {} {}".format(i,j-1))
        if j<self.dimension-1:
            if self.board[i][j+1]!="X":
                if self.IsSideEffect(i,j+1):
                    self.mboard[self.board[i][j+1]].remove([i,j+1])
                    self.board[i][j+1]="X"
                    # print("Side effect {} {}".format(i,j+1))

    def Move(self,player,i,j):
        if self.color[player]==self.board[i][j]:
            self.mboard[self.color[player]].remove([i,j])
            self.SideEffect(i,j)
            self.board[i][j]="X"
            return True
        else:
            return False

    def GameOver(self):
        if self.mboard[self.color[0]]==[]:
            if self.mboard[self.color[1]]==[]:
                print("Draw")
                return True
            else:
                print("You win")
                return True
        if self.mboard[self.color[1]]==[]:
            print("AI win")
            return True
        return False

    def play(self):
        while 1:
            first=input("User goes first or not (Y/N) : \n").upper()
            if (first=="Y" or first=="N"):
                break
            else:
                print("wrong input")
        while 1:
            color=input("Enter your color (B/R) : \n").upper()
            if color=="B":
                self.color=["B","R"]
                break
            elif color=="R":
                self.color=["R","B"]
                break
            else:
                print("wrong input")
        if first=="Y":
            while 1:
                I=input("User ==> Enter row column : \n").split()
                if len(I)!=2:
                    print("wrong input")
                else:
                    if self.Move(0,int(I[0]),int(I[1])):
                        break
                    else:
                        print("Illegal movement")
        for r in self.board:
            print(' '.join(r))
        while 1:
            i,j=self.DecideNextMove()
            print("AI move {} {} ".format(i,j))
            self.Move(1,i,j)
            for r in self.board:
                print(' '.join(r))
            if self.GameOver():
                break
            while 1:
                I=input("User ==> Enter row column : \n").split()
                if len(I)!=2:
                    print("wrong input")
                else:
                    if self.Move(0,int(I[0]),int(I[1])):
                        for r in self.board:
                            print(' '.join(r))
                        break
                    print("Illegal movement")
            if self.GameOver():
                break

if __name__ == "__main__":
    while 1:
        board=input("Please input the type of the board : \n1 : 4x4 | 2 : 10x10 | 3 : others\n")
        if board=="1":
            A=Agent("test_n4.txt")
            break
        elif board=="2":
            A=Agent("test_n10.txt")
            break
        elif board=="3":
            name=input("Please input the name of the test file : \n")
            if exists(name):
                A=Agent(name)
                break
            else:
                print("File not exist")
    A.play()