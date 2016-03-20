from contextlib import suppress
from math import sqrt
import random

# Question 1.1: randsat: 
args = [(10, 2, 5), (3, 3, 3), (5, 3, 5), (4, 3, 9), (3, 3, 12), (3, 3, 20)]
# Question 1.2, 1.3: satcom, satcomfast: 
CNF = {'easy':[[1, 3, 2], [-1, 3, 2], [3, 1, -2]],
     'hard':[[1, 2, 3], [-1, -3, -2], [-1, -2, -3], [-3, -1, -2], [2, 1, -3], [3, 2, 1], 
             [-3, 2, -1], [3, 2, 1], [-1, 3, 2], [-2, 3, 1], [-2, -3, 1], [3, 2, 1]],
     'border':[[-3, 1, -2], [-1, 3, 2], [-3, 1, -2], [-1, 3, 2], [2, 1, -3], [-2, -3, -1], [-3, 2, 1], 
               [-3, -2, -1], [-1, 3, -2], [-1, 2, 3], [-1, -2, -3], [-2, 1, -3], [-3, 2, 1], 
               [1, 3, -2], [3, -1, 2], [-1, 2, 3], [-1, -2, -3], [-2, -3, 1], [2, 1, 3], [2, -3, -1]],
     'easy_long':[[9, 2], [-10, -5], [-5, -2], [-2, -5], [2, -8]],
     'unsat':[[1, -2], [-1, -2], [-1, 2], [1, 2]],
     'other': [],
     'patho': [[],[]]
     }


def confirm(cnf, asg):
    """
    Return T iff asg satisfies cnf
    Otherwise print offending clause and return F
    
    >>> confirm(CNF['easy'], [0, 0, 0, 1])
    True
    >>> confirm(CNF['easy'], [0, 1, 1, 0])
    True
    >>> confirm(CNF['easy'], [0, -1, 1, 1])
    True
    >>> confirm(CNF['easy'], [0, -1, -1, 1])
    True
    >>> confirm(CNF['easy'], [0, 1, -1, -1])
    Asg [0, 1, -1, -1] doesn't satisfy clause [-1, 3, 2]
    False
    """
    for clause in cnf:
        for lit in clause:
            if asg[abs(lit)] * lit > 0:
                break
        else:
            print("Asg {} doesn't satisfy clause {}".format(asg, clause))
            return False
    return True

def get_max_lit(cnf):
    """
    Return the largest literal in the statement
    
    >>> get_max_lit(CNF['easy'])
    3
    >>> get_max_lit(CNF['easy_long'])
    10
    """
    with suppress(ValueError):
        return max([max(map(abs, x)) for x in cnf])
    

def get_min_len(cnf):
    """
    Return the length of the shortest clause
    
    >>> get_min_len([[]])
    0
    >>> get_min_len([[1, 2], [1]])
    1
    """
    with suppress(ValueError):
        return min(map(len, cnf))

def get_next_lit(cnf):
    """
    Return the next literal in the CNF
    
    >>> get_next_lit(CNF['easy'])
    1
    >>> get_next_lit(CNF['border'])
    3
    """
    for clause in cnf:
        if len(clause) > 0:
            return abs(clause[0])


def check_consistent(cnf):
    """
    Return a literal that only appears in one form
    
    >>> check_consistent([[1, 2], [-1, -2]])
    >>> check_consistent([[1, 2], [1, -2]])
    1
    >>> check_consistent([[1, 2, 3], [-2, -3, 4], [2, 3, -4]])
    1
    """
    # find all the literals that occur positively
    pos = set([x for clause in cnf for x in clause if x > 0 ])
    # find all the literals that occur negatively
    neg = set([abs(x) for clause in cnf for x in clause if x < 0])

    # now get rid of the ones that appear both positively and negatively
    diff = pos.symmetric_difference(neg)
    
    # if there are any, return one with appropriate sign
    if len(diff) > 0:
        l = diff.pop()
        if l in pos:
            return l
        else:
            return -1 * l
        
                

def get_lonely_lit(cnf):
    """
    Return the first literal that appears alone in a clause
    
    >>> get_lonely_lit([[1], [1, 2, 3], [2]])
    1
    >>> get_lonely_lit([[], [-2], [1, 2, 3]])
    -2
    """
    for clause in cnf:
        if len(clause) == 1:
            return clause[0]


def satcomfast(C, assign=None):
    """
    Find an assignment that satisfies or falsifies C
    
    >>> satcomfast([], [0])
    [0]
    >>> satcomfast([[1]])
    [0, 1]
    >>> print(satcomfast([[-1]]))
    [0, -1]
    >>> confirm([[-1, 2], [1, 2]], satcomfast([[-1, 2], [1, 2]]))
    True
    >>> confirm(CNF['easy'], satcomfast(CNF['easy']))
    True
    >>> print(satcomfast(CNF['unsat']))
    None
    >>> confirm(CNF['easy_long'], satcomfast(CNF['easy_long']))
    True
    >>> confirm(CNF['hard'], satcomfast(CNF['hard']))
    True
    """
    if len(C) == 0: # 0-clause is satisfied
        return assign 
    elif get_min_len(C) == 0: # cnf with 0-length clause is unsatisfiable
        return None
    elif assign == None: # if this is the first call we need to set up the possibilities
        max_lit = get_max_lit(C)
        assign = [0]*(max_lit+1)
    
    # if there is a lone literal we know what we need to do
    lit = get_lonely_lit(C)
    if lit:
        if lit > 1:
            assign[lit] = 1
            r = satcomfast(satcom_apply_true(C, lit), assign)
        else:
            assign[lit] = -1
            r = satcomfast(satcom_apply_false(C, lit), assign)
        # did it work?
        if r is not None:
            return r
    
    # if there isn't, we should check if there's one that only appears in one form
    lit = check_consistent(C)
    if lit:
        if lit > 1:
            assign[lit] = 1
            r = satcomfast(satcom_apply_true(C, lit), assign)
        else:
            assign[lit] = -1
            r = satcomfast(satcom_apply_false(C, lit), assign)
        # did it work?
        if r is not None:
            return r
    
    # and if that fails, just get the next one
    lit = get_next_lit(C)

    # and try making it False
    assign[lit] = -1
    r = satcomfast(satcom_apply_false(C, lit), assign)
    
    # if that didn't work, try making it True
    if r is None:
        assign[lit] = 1
        r = satcomfast(satcom_apply_true(C, lit), assign)
    
    # return the results up the stack
    return r


def randsat(n, k, m):
    if n < k: # make sure that we have enough literals for k unique choices
        raise ValueError("Number of literals must exceed clause size.")
    lits = range(1, n+1)
    signs = [-1, 1]
    c = []
    for _ in range(m):
        clause = [random.choice(signs)*r for r in random.sample(lits, k)]
        c.append(clause)
    return c
    
def satcom(C, assign=None):
    """
    Find an assignment that satisfies or falsifies C
    
    >>> print(satcom([[],]))
    None
    >>> satcom([])
    []
    >>> satcom([[1]])
    [0, 1]
    >>> print(satcom([[-1]]))
    [0, -1]
    >>> satcom([[-1, 2], [1, 2]])
    [0, -1, 1]
    >>> satcom(CNF['easy'])
    [0, -1, 1, 1]
    >>> print(satcom(CNF['unsat']))
    None
    """
    if len(C) == 0: # 0-clause is satisfied
        if assign is not None:
            return assign 
        else:
            return []
    elif get_min_len(C) == 0: # cnf with 0-length clause is unsatisfiable
        return None
    elif assign == None: # if this is the first call we need to set up the possibilities
        max_lit = get_max_lit(C)
        assign = [0]*(max_lit+1)

    # try making one False    
    lit = get_next_lit(C)
    assign[lit] = -1
    r = satcom(satcom_apply_false(C, lit), assign)
    
    # if that didn't work, try making it True
    if r is None:
        assign[lit] = 1
        r = satcom(satcom_apply_true(C, lit), assign)
    
    # return the results up the stack
    return r
    

def satcom_apply_false(C, lit):
    """
    Return a new statement resulting from setting lit to False

    >>> satcom_apply_false([[1, 3, 2], [-1, 3, 2], [3, 1, -2]], 1)
    [[3, 2], [3, -2]]
    
    """
    new_C = []
    for clause in C:
        if (-1 * lit) in clause: # skip clauses that are now satisfied
            continue
        else: # append clauses but skip literals that are already False
            new_C.append([l for l in clause if l != lit]) 
    return new_C

def satcom_apply_true(C, lit):
    """
    Return a new statement resulting from setting lit to True
    
    >>> satcom_apply_true([[1, 3, 2], [-1, 3, 2], [3, 1, -2]], 1)
    [[3, 2]]
    """
    new_C = []
    for clause in C:
        if lit in clause: # skip classes that are satisfied
            continue
        else: # append all other clauses, but skip literals that are set False by this
            new_C.append([l for l in clause if l != -1 * lit])
    return new_C
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Done")
    
               
                