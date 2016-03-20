from contextlib import suppress
from math import sqrt
import random

ACTIONS = ['u', 'd', 'l', 'r']
SOLVED_EIGHT = (1, 8, 7, 2, 0, 6, 3, 4, 5)


def calc_move(action, state, board_size=3):
    """
    Return a tuple of the board positions to swap given the action and state passed.
    
    >>> calc_move('u', SOLVED_EIGHT)
    (4, 3)
    >>> calc_move('d', SOLVED_EIGHT)
    (4, 5)
    >>> calc_move('l', SOLVED_EIGHT)
    (4, 1)
    >>> calc_move('r', SOLVED_EIGHT)
    (4, 7)
    >>> calc_move('r', [1, 8, 7, 2, 5, 6, 3, 4, 0])
    (8, 8)
    >>> calc_move('d', [1, 8, 7, 2, 5, 6, 3, 4, 0])
    (8, 8)
    >>> calc_move('u', [1, 8, 7, 2, 5, 6, 3, 4, 0])
    (8, 7)
    >>> calc_move('l', [1, 8, 7, 2, 5, 6, 3, 4, 0])
    (8, 5)
    """
    loc1 = state.index(0)
    loc2 = loc1

    if action == 'u': # move up by swapping backwards in array unless at boundaries
        if loc1 % board_size != 0:
            loc2 = loc1 - 1
    elif action == 'd': # move down by swapping forwards
        if loc1 % board_size != board_size-1:
            loc2 = loc1 + 1
    elif action == 'l': # move left by setting it one column back
        if loc1 - board_size >= 0:
            loc2 = loc1 - board_size
    elif action == 'r': # move right by setting it one column forward
        if loc1 + board_size < len(state):
            loc2 = loc1 + board_size
    return (loc1, loc2)
    
def apply_move(action, state, board_size=3):
    """
    Alter the state list by applying the action given

    >>> state = list(SOLVED_EIGHT)
    >>> apply_move('u', state); state
    [1, 8, 7, 0, 2, 6, 3, 4, 5]
    >>> apply_move('d', state); state
    [1, 8, 7, 2, 0, 6, 3, 4, 5]
    >>> apply_move('l', state); state
    [1, 0, 7, 2, 8, 6, 3, 4, 5]
    >>> apply_move('r', state); state
    [1, 8, 7, 2, 0, 6, 3, 4, 5]
    >>> apply_move('r', state); state
    [1, 8, 7, 2, 4, 6, 3, 0, 5]
    >>> apply_move('r', state); state
    [1, 8, 7, 2, 4, 6, 3, 0, 5]
    >>> apply_move('u', state); state
    [1, 8, 7, 2, 4, 6, 0, 3, 5]
    >>> apply_move('u', state); state
    [1, 8, 7, 2, 4, 6, 0, 3, 5]
    """
    (l1, l2) = calc_move(action, state, board_size=board_size)
    state[l1], state[l2] = state[l2], state[l1]

def apply_moves(actions, state):
    """
    Apply a sequence of moves
    
    >>> state = list(SOLVED_EIGHT)
    >>> apply_moves('du', state)
    >>> compare(state, SOLVED_EIGHT)
    True
    >>> apply_moves('ul', state)
    >>> state
    [0, 8, 7, 1, 2, 6, 3, 4, 5]
    """
    for a in actions:
        apply_move(a, state)

    
def copy_move(action, state, board_size=3):
    """
    Return a copy of the state with the action applied
    
    >>> copy_move('u', SOLVED_EIGHT)
    [1, 8, 7, 0, 2, 6, 3, 4, 5]
    """
    state = [n for n in state]
    (l1, l2) = calc_move(action, state, board_size=board_size)
    state[l1], state[l2] = state[l2], state[l1]
    return state

def copy_moves(actions, state):
    """
    Return a copy of the state with the actions applied
    """
    state = [s for s in state]
    apply_moves(actions, state)
    return state

def compare(state, other):
    """
    Return True iff the current game state is the final solution
    
    >>> start = list(SOLVED_EIGHT)
    >>> compare(SOLVED_EIGHT, start)
    True
    >>> compare(start, [1, 8, 7, 0, 2, 6, 3, 4, 5])
    False
    >>> apply_move('u', start)
    >>> compare(start, SOLVED_EIGHT)
    False
    >>> compare(start, [1, 8, 7, 0, 2, 6, 3, 4, 5])
    True
    """
    return all(x == y for (x, y) in zip(state, other))

def randep(d):
    """
    Return a random instance of the sliding puzzle.
    """
    state = list(SOLVED_EIGHT)
    for _ in range(d):
        apply_move(random.choice(ACTIONS), state)
    return state

def ids(s, g=SOLVED_EIGHT):
    """
    Given a start state s and a goal state g, return the shortest path of moves
    that gets you from start to goal, in the 8 puzzle.
    
    >>> ids(SOLVED_EIGHT, SOLVED_EIGHT)
    []
    >>> ids(copy_move('u', SOLVED_EIGHT), SOLVED_EIGHT)
    ['d']
    >>> ids(copy_moves('ur', SOLVED_EIGHT), SOLVED_EIGHT)
    ['l', 'd']
    >>> ids(copy_moves('ul', SOLVED_EIGHT), SOLVED_EIGHT)
    ['r', 'd']
    >>> ids(copy_moves('dlu', SOLVED_EIGHT), SOLVED_EIGHT)
    ['d', 'r', 'u']
    >>> ids(copy_moves('dluu', SOLVED_EIGHT), SOLVED_EIGHT)
    ['d', 'd', 'r', 'u']
    """
    # using prior knowledge about 8 puzzles to limit the depth
    for d in range(32):
        result = dls(s, g, d)
        if result is not None:
            return result      

# compute the distance map, a 9x9 matrix for minimum number of moves from i to j
distance_map = [[0]*9 for _ in range(9)]
for i, row in enumerate(distance_map):
    for j in range(9):
        if i == j:
            continue
        # moving into the same column is the difference in their column index
        row[j] = abs((i // 3) - (j // 3))
        # moving into the same row is the difference in row index
        row[j] += abs((i % 3) - (j % 3))        

def piece_distance(s, g):
    """
    Return the total number of independent moves it would take to get
    the pieces from their s position to their g position
    
    >>> piece_distance(SOLVED_EIGHT, SOLVED_EIGHT)
    0
    >>> piece_distance([1, 8, 7, 2, 6, 0, 3, 4, 5], SOLVED_EIGHT)
    2
    >>> piece_distance(copy_moves('ur', SOLVED_EIGHT), SOLVED_EIGHT)
    4
    """
    total = 0
    for i in range(9):
        total += distance_map[s.index(i)][g.index(i)]
    return total
        
    

def idas(s, g=SOLVED_EIGHT):
    """
    Given a start state s and a goal state g, return the shortest path of moves
    that gets you from start to goal, in the 8 puzzle.
    
    Use a heuristic to determine the ordering of actions to search
    
    >>> idas(SOLVED_EIGHT, SOLVED_EIGHT)
    []
    >>> idas(copy_move('u', SOLVED_EIGHT), SOLVED_EIGHT)
    ['d']
    >>> idas(copy_moves('ur', SOLVED_EIGHT), SOLVED_EIGHT)
    ['l', 'd']
    >>> idas(copy_moves('ul', SOLVED_EIGHT), SOLVED_EIGHT)
    ['r', 'd']
    >>> idas(copy_moves('dlu', SOLVED_EIGHT), SOLVED_EIGHT)
    ['d', 'r', 'u']
    >>> idas(copy_moves('dluu', SOLVED_EIGHT), SOLVED_EIGHT)
    ['d', 'd', 'r', 'u']
    """
    # using prior knowledge about 8 puzzles to limit the depth
    for d in range(32):
        result = dls(s, g, d, heuristic=piece_distance)
        if result is not None:
            return result      
    

def dls(s, g=SOLVED_EIGHT, d=1, heuristic=None, actions=ACTIONS):
    """
    Given a start state s and a goal state g, do depth-limited search
    Return a list of successful actions
    If a heuristic function is provided then use that to order the search. Otherwise
    use action ordering provided.
    
    >>> dls(SOLVED_EIGHT, SOLVED_EIGHT)
    []
    >>> dls(copy_move('u', SOLVED_EIGHT), SOLVED_EIGHT)
    ['d']
    >>> dls(copy_move('u', SOLVED_EIGHT), SOLVED_EIGHT, actions=['l', 'u'])
    >>> dls(copy_moves('ur', SOLVED_EIGHT), SOLVED_EIGHT, 2)
    ['l', 'd']
    >>> dls(copy_moves('ur', SOLVED_EIGHT), SOLVED_EIGHT, 3)
    ['u', 'l', 'd']
    >>> dls(copy_moves('ur', SOLVED_EIGHT), SOLVED_EIGHT, 3, actions=['l', 'd', 'r', 'u'])
    ['l', 'd']
    >>> dls(copy_moves('ul', SOLVED_EIGHT), SOLVED_EIGHT, 2)
    ['r', 'd']
    >>> dls(copy_moves('dlu', SOLVED_EIGHT), SOLVED_EIGHT, 3)
    ['d', 'r', 'u']
    >>> dls(copy_moves('dluu', SOLVED_EIGHT), SOLVED_EIGHT, 4)
    ['d', 'd', 'r', 'u']
    """
    # check if we're at the goal
    if compare(s, g):
        return [] # this will successfully add to a list
    if d <= 0: # not at the goal and out of depth
        return None
    
    # compute all the possible next nodes
    states = {}
    vals = {}
    for a in actions:
        states[a] = copy_move(a, s)

        # check if this is the goal
        if compare(states[a], g):
            return [a] # return the successful action
        
        # store the heuristic value if we hae it
        if heuristic: 
            vals[a] = heuristic(states[a], g)

    # if we don't have any depth left, we're done.
    if d <= 1:
        return None

    # re-order the actions if we have a heuristic
    if vals:
        actions = sorted(vals, key=vals.get)
    
    # try searching from each action
    for a in actions:
        with suppress(TypeError): # only return is this action is not a dead end
            return [a] + dls(states[a], g, d-1, actions=actions, heuristic=heuristic)
        # otherwise try the next state
    # now we've tried all the actions without getting a success
    return None # this state is a dead end

idasfast = idas
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Done")

                
                