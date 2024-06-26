# https://www.javatpoint.com/mini-max-algorithm-in-ai (contains pseudo code for minimax algo)

# Minmax at line 155
# TODO - bot is what color
# - which color is associated with which value of terminal nodes
# - implement alpha-beta pruning
# - Currently im writing the code where the simulated_game function does all the work, 
# theres probably a way to use both functions later 

from collections import defaultdict, deque
from functools import partial
from itertools import count, repeat, compress
from operator import eq
from enum import StrEnum

import matplotlib.pyplot as plt
import networkx as nx


class Color(StrEnum):
    R = RED = "red"
    B = BLUE = "blue"

    @property
    def other(self):
        if self is Color.R:
            return Color.B
        else:
            return Color.R


BranchDict = dict[Color, dict[int, set[int]]]


def get_edges(branches: BranchDict):
    """get a list of edges and colors from a dictionary of branches"""
    seen = {0}
    remaining = deque(seen)

    edges = []
    colors = []

    # bfs since colors need to be specified in this order to draw correctly
    while remaining:
        curr = remaining.popleft()
        for c in Color:
            new_vertices = branches[c][curr] - seen

            seen.update(new_vertices)
            remaining.extend(new_vertices)

            edges.extend(zip(repeat(curr), new_vertices))
            colors.extend(repeat(c, len(new_vertices)))

    return edges, colors


def get_branches(edges, colors, chosen=None):
    """get a dictionary of branches from edges and colors and a banned edge"""

    branches: BranchDict = {}
    for color in Color:
        branches[color] = defaultdict(set)

    for i, ((a, b), color) in enumerate(zip(edges, colors), 1):
        if i == chosen:
            continue

        branches[color][a].add(b)
        branches[color][b].add(a)

    return branches


def draw_graph(graph: nx.Graph, pos, edges, colors):
    """draw a game of hackenbush"""
    graph.clear()

    nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color=colors)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=dict(map(reversed, enumerate(edges, 1))))

    plt.show()


def get_branch_choice(possible, player):
    print(f"{player}'s turn")
    print(f"possible moves: {possible}")
    while True:
        try:
            chosen_str = input("enter branch to cut or q to exit: ")

            # exit if q is chosen
            if chosen_str == "q":
                return None

            # retry if the chosen branch is invalid
            chosen = int(chosen_str)
            if chosen not in possible:
                raise ValueError
        except ValueError:
            print("invalid branch")
            continue

        return chosen


def game(edges, colors, player: Color, drawer):
    """play a game of hackenbush"""
    # get a list of all the branches of the correct color
    possible = list(compress(count(1), map(partial(eq, player), colors)))

    # if the player can't make a move, the other one wins
    if not possible:
        print(f"{player.other} wins")
        return

    # get a branch to cut
    chosen = get_branch_choice(possible, player)

    # exit if requested
    if chosen is None:
        return

    # get the branches that didn't fall
    edges, colors = get_edges(get_branches(edges, colors, chosen))

    # draw the graph
    drawer(edges, colors)

    # continue the game
    game(edges, colors, player.other, drawer)

def simulated_game(edges, colors, player: Color):
    '''Simulated game used by the minmax bot. If the position is won for blue, 
    it is a terminal node with value of +infinity, the inverse is true for read.'''
    possible = list(compress(count(1), map(partial(eq, player), colors)))

    # Triggers at terminal node, value of -100 for win for blue (player), 100 for red (bot)
    if not possible:
        if player == Color.BLUE: # Player loses 
            return 100, []
        else: # Bot loses
            return -100, []
    
    eval = [] # List of evaluations (branch, value) for every subsequent 'games' that could occur next 

    # Searches through every game in an dfs manner (implement alpha-beta pruning later)
    for branch in possible:
        chosen = branch 
        edges, colors = get_edges(get_branches(edges, colors, chosen))

        # dfs occurs
        value, moves = simulated_game(edges, colors, player.other)

        # moves are the set of branches cut assuming perfect play from both parties
        moves.append(branch)
        eval.append(moves, value)

    # Minimizing agent (player)
    if player == Color.Blue:




def minmax(node, depth, color): # Why is there an error?
    '''Minmax algorithm implemented with recursion. 
    The depth value should only matter when the bot has a losing position to prolong the game. 
    The node variable is equivalent to a possible game state. 
    '''
    return 

# add branches for simulation
edges, colors = zip(*(
    ((0, 1), Color.B),
    ((1, 2), Color.R),
    ((1, 3), Color.B),
    ((3, 4), Color.R),

    ((0, 5), Color.R),
    ((5, 6), Color.B)
))

# reorder the edges to draw them correctly
edges, colors = get_edges(get_branches(edges, colors))

# create a graph
graph = nx.Graph(edges)

# set the way the graph is displayed
pos = nx.bfs_layout(graph, 0, align="horizontal")
drawer = partial(draw_graph, graph, pos)

# draw the graph
drawer(edges, colors)

# start the game
game(edges, colors, Color.BLUE, drawer)

