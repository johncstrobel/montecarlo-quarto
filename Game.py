import os,sys,random
from Totem import Totem
from Board import Board

class Game:
    def __init__(self,n):
        # set up array of pieces
        self.piecesleft = []
        max = pow(2,n)
        for i in range(max):
            t = Totem(n)
            t.setIDInt(i,n)
            self.piecesleft.append(t)

        #reduce total pieces randomly until # pieces = # board spaces
        random.shuffle(self.piecesleft)
        if(max > pow(n,2)):
            for i in range(max - pow(n,2)):
                self.piecesleft.pop()

        # set up board
        self.board = Board(n)

    def __repr__(self):
        return str(self.board)

    def CheckGameEnd(self):
        # check columns
        col = self.board.columns()
        row = self.board.rows()
        d1 = self.board.diagonalLeft()
        d2 = self.board.diagonalRight()
        stillmatching = True

        for column in col: # for each column
            stillmatching = True
            for element in column:
                if(element is None or not stillmatching):
                    stillmatching = False
                    break
                for second in column:
                    if(second == element):
                        continue
                    if(second is None or not stillmatching):
                        stillmatching = False
                        break
                    if(element.match(second)):
                        continue
                    else:
                        stillmatching = False
            if(stillmatching):
                return "col"

        for r in row:
            stillmatching = True
            for element in r:
                if(element is None or not stillmatching):
                    stillmatching = False
                    break
                for second in r:
                    if(second == element):
                        continue
                    if(second is None or not stillmatching):
                        stillmatching = False
                        break
                    if(element.match(second)):
                        continue
                    else:
                        stillmatching = False
            if(stillmatching):
                return "row"

        stillmatching = True
        for element in d1:
            if(element is None or not stillmatching):
                stillmatching = False
                break
            for second in d1:
                if(second == element):
                    continue
                if(second is None or not stillmatching):
                    stillmatching = False
                    break
                if(element.match(second)):
                    continue
                else:
                    stillmatching = False
        if(stillmatching):
            return "left diagonal"

        stillmatching = True
        for element in d2:
            if(element is None or not stillmatching):
                stillmatching = False
                break
            for second in d2:
                if(second == element):
                    continue
                if(second is None or not stillmatching):
                    stillmatching = False
                    break
                if(element.match(second)):
                    continue
                else:
                    stillmatching = False
        if(stillmatching):
            return "right diagonal"

        if(len(self.piecesleft) == 0):
            return "draw"
        return False

    def UserAddPieceToBoard(self,piece,p): # the version that has UI in it
        # validation on piece placement TODO
        validchoice = False
        while(not validchoice):
            print("=====Player ",p,"=====\n Choose coordinates to place the piece.\n\t", piece)
            x = input("choose x ")
            y = input("choose y ")
            validchoice = self.AddPieceToBoard(piece,x,y)

    def AddPieceToBoard(self,piece,x,y):
        if(self.board.addPiece(piece,int(x),int(y))):
            return True
        else:
            print("invalid piece placement, try again")
            print(x,y)
            print(piece)
            print(self.board)
            return False
            # piece placed on top of another piece

    def GetPieceLocation(self,piece):
        return self.board.piecelocation(piece)

    def UserDisplayPieces(self):
        for i in range(len(self.piecesleft)):
            print(i,": ",self.piecesleft[i])

    def UserDisplayBoard(self):
        print(self.board)

    def UserChoosePiece(self,p):
        print("=====Player ",p,"=====\nChoose your piece: ",end = '')
        temp = input()
        p = int(temp)
        piece = g.piecesleft[p]
        del g.piecesleft[p]
        return piece

    def UserDisplayGameEnd(self,p):
        print("  ####     ##    #    #  ######     ")
        print(" #    #   #  #   ##  ##  #          ")
        print(" #       #    #  # ## #  #####      ")
        print(" #  ###  ######  #    #  #          ")
        print(" #    #  #    #  #    #  #          ")
        print("  ####   #    #  #    #  ######     \n")
        print("  ####   #    #  ######  #####  ")
        print(" #    #  #    #  #       #    # ")
        print(" #    #  #    #  #####   #    # ")
        print(" #    #  #    #  #       #####  ")
        print(" #    #   #  #   #       #   #  ")
        print("  ####     ##    ######  #    # \n\n")
        print("Player ", p, " wins!")


        self.DisplayGameEnd(p)


        #TODO: add functionality

    def DuplicatesExist(self):
        return self.board.duplicatesexist()

    def DisplayGameEnd(self,p):
        self.UserDisplayBoard()
        #TODO: print winning row/column/diaganal

    def CPUDisplayBoard(self):
        return self.board

    def CPUAvailablePieces(self):
        return self.piecesleft

    def CPUAvailableSpaces(self):
        return self.board.emptyspaces()

    def GetRandomPiece(self):
        x = random.randint(0,len(self.piecesleft)-1)
        return self.piecesleft[x]

    def UserGame(self,size):
        # set up class
        g = Game(int(size))
        player = 1
        while(True):
            # clear screen
            clear = lambda: os.system('clear')
            clear()

            # print new board
            g.UserDisplayBoard()

            # display available pieces
            g.UserDisplayPieces()

            # prompt for piece choice
            piece = g.UserChoosePiece(player)

            print(player)
            #switch player
            if(player == 1):
                player = 2
            elif(player == 2):
                player = 1

            # prompt for piece placement
            g.UserAddPieceToBoard(piece, player)

            end = g.CheckGameEnd()
            if(end):
                print(end)
                g.UserDisplayGameEnd(player)
                break


        print("game exiting normally")
