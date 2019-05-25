from MCTS import monte_carlo_tree_search
from Game import Game
from Node import Node
import sys,random,csv,time

################################################################################
#    MAIN     ##################################################################
################################################################################

#arguments from command line:
#board size, user interface, max nodes, max time seconds,
# if(len(sys.argv) < 6):
#     print(len(sys.argv))
#     print("usage: Main.py <board size start> <board size stop> <board size step> <max nodes> <max time in seconds> <user interface>")
#     quit()
# size1 = sys.argv[1]

# PROBLEMS # TODO
# game can place two of the same piece on the board
#
# number of pieces can exceed places on the board: fix this (limit to n^2 instead of 2^n pieces)

def playgame(n,maxtime,maxnodes,defaultmaxtime=1.0, defaultmaxnodes=1250): # plays an entire game and returns results

    g = Game(n)
    nextpiece = g.GetRandomPiece() # does not matter which piece starts
    player = random.randint(0,1) # even = variable AI, odd = control AI

    # stats
    sp = None
    if(player % 2 == 0):
        sp = "v"
    else:
        sp = "c"
    variableelapsed = 0
    controlelapsed = 0
    variablenodes = 0
    controlnodes = 0

    while (not g.CheckGameEnd()):
        if(player % 2 == 0): # variable AI
            #  pass piece & game to root
            root = Node(game = g, piece = nextpiece)

            #  pass root & constraints to MCTS
            choice = monte_carlo_tree_search(maxtime,maxnodes,root)
            piece = choice[3].piece
            space = choice[1]
            x = g.AddPieceToBoard(nextpiece,space[0],space[1])
            nextpiece = choice[0]

            #stats
            variableelapsed += choice[4]
            variablenodes += choice[5]
        else: # control AI
            #  pass piece & game to root
            root = Node(game = g, piece = nextpiece)

            #  pass root & constraints to MCTS
            choice = monte_carlo_tree_search(defaultmaxtime,defaultmaxnodes,root)
            piece = choice[3].piece
            space = choice[1]
            x = g.AddPieceToBoard(nextpiece,space[0],space[1])
            nextpiece = choice[0]

            #stats
            controlelapsed += choice[4]
            controlnodes += choice[5]
        player += 1

    winner = None
    if(player % 2 == 0): # last player to act = winner
        winner = "v"
    else:
        winner = "c"
    dict = {"board size":n,"variable max nodes":maxnodes,"variable max time":'%.3f'%(maxtime),
        "start player":sp,"winner":winner,
        "control time":'%.3f'%(controlelapsed),"variable time":'%.3f'%(variableelapsed),
        "control nodes":controlnodes,"variable nodes":variablenodes}
    return dict

def collectdata(writer):
    overall_trial = 1
    maxtime = 1.0 # maxtime fixed to increase total trials
    for boardsize in range(6,15): #traverse board sizes
        for maxnodes in [1000,1250,1500]: #traverse max nodes
            for i in range(10): #repeat each trial a few times
                s = time.time()
                dict = playgame(boardsize,maxtime,maxnodes)
                f = time.time()
                dict.update({"iteration":i,"total time":'%.3f'%(f-s),"trial":overall_trial})
                writer.writerow(dict)
                print((("="*80)+"\n")*3)
                print(dict)
                overall_trial += 1

with open('data.csv','w',newline = '\n') as csvfile:
    fieldnames = ["trial","board size","variable max time","variable max nodes","iteration",
        "total time",
        "start player","winner",
        "control time","variable time",
        "control nodes","variable nodes"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    collectdata(writer)
    csvfile.close()
print((("="*80)+"\n")*3)
print("exiting normally")
