from Game import Game
import math, copy, random, sys, time

class Node:
    def __init__(self,parent = None, piece = None, game = None):
        self.parent = parent
        self.piece = piece # piece given by parent (add to board when spawning children)
        self.stats = [0,0] # wins, visits
        self.actions = []
        self.children = []
        self.score = float('inf')
        self.game = game

        if parent is not None:
            self.is_root = False
            self.parentpiece = parent.piece # piece given to parent, already added to board
        else:
            self.is_root = True
            self.parentpiece = None

        # propagate actions
        if(self.game is not None):
            pieces = self.game.CPUAvailablePieces()
            pieces.remove(self.piece)
            for p in pieces:
                for space in self.game.CPUAvailableSpaces():
                    self.actions.append([p,space])

    def __repr__(self):
        return "(" + str(self.game.board) + ", " + str(self.piece) + ")"

    def rollout(self): # places remaining pieces randomly until board is filled
        player = 0 # even = self; odd = other
        rolloutgame = copy.deepcopy(self.game)
        spaces = copy.deepcopy(self.game.CPUAvailableSpaces())
        pieces = copy.deepcopy(self.game.CPUAvailablePieces())
        while(len(spaces) > 0 and len(pieces) > 0):
            nextspaceint = random.randint(0,len(spaces)-1)
            nextpieceint = random.randint(0,len(pieces)-1)
            nextspace = spaces[nextspaceint]
            nextpiece = pieces[nextpieceint]
            x = rolloutgame.AddPieceToBoard(nextpiece, nextspace[0], nextspace[1])

            end = rolloutgame.CheckGameEnd()
            if(end):
                if player % 2 == 0 and end != "draw":
                    return True
                else: # lose or draw
                    return False
            player = player + 1
            del spaces[nextspaceint]
            del pieces[nextpieceint]
        return False # ???

    def backpropagate(self,result):
        if(result):
            self.stats[0] += 1
        self.stats[1] += 1
        if(self.is_root):
            return
        self.parent.backpropagate(result)

    def is_terminal_node(self):
        if(len(self.children)==0 and len(self.actions)==0):
            return True
        return False

    def is_fully_expanded(self):
        if(len(self.actions) == 0):
            return True
        return False

    def expand(self):
        if(not self.is_fully_expanded()):
            nextaction = random.randint(0,len(self.actions)-1)
            nextpiece = self.actions[nextaction][0]
            nextspace = self.actions[nextaction][1]

            #copy current game
            nextgame = copy.deepcopy(self.game)

            #add given piece to copy in random space
            nextgame.AddPieceToBoard(self.piece, nextspace[0], nextspace[1]) # self.piece = given piece

            #make child with modified game copy and random piece
            n = Node(parent = self, piece = nextpiece, game = nextgame)
            self.children.append(n)

            del self.actions[nextaction]
            return True
        else: return False

    def best_child(self): # chooses most visited (aka most successful) child
        max = -1
        best = None
        random.shuffle(self.children)
        for c in self.children:
            if max < c.stats[1]:
                max = c.stats[1]
                best = c
        return best

    def calculate_uct(times,wins,parenttimes):
        if(parenttimes == 0 or times == 0):
            return float('inf')
        return ((wins / times) + (math.sqrt((2 * math.log(parenttimes))/(times))))

    def best_uct(self): # chooses child with highest UCT score
        times = self.stats[1]
        max = self.children[0]
        for c in self.children:
            c.score = Node.calculate_uct(c.stats[1],c.stats[0], times)
            if(c.score > max.score):
                max = c
        return max
