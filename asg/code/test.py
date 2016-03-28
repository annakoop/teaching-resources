from contextlib import suppress
from functools import partial
from math import sqrt
import random
import timeit

args = [(10, 2, 5), (3, 3, 3), (5, 3, 5), (4, 3, 9), (3, 3, 12), (3, 3, 20)]

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


EIGHT = {'onem': [1, 8, 7, 2, 6, 0, 3, 4, 5],
         'easy': [1, 8, 7, 3, 0, 2, 4, 5, 6],

         'correct': [1, 8, 7, 2, 0, 6, 3, 4, 5],
         #'reg':     [1, 4, 7, 2, 5, 8, 3, 6, 0],

         #'other': [8, 2, 3, 6, 5, 0, 7, 4, 1],
         #'another': [6, 8, 3, 4, 5, 2, 7, 0, 1],

         #'hard1': [8, 4, 3, 6, 1, 2, 7, 0, 5],
         #'hard2': [6, 0, 3, 4, 1, 8, 7, 2, 5],
         }

SOLVED_EIGHT = [1, 8, 7, 2, 0, 6, 3, 4, 5]


###### SAT testing - Question 1
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

def test_simple_sats(func):
    for k in CNF:
        print("Testing {}".format(k))
        try:
            ans = func(CNF[k])
        except Exception as e:
            ans = None
            print("RAISED EXCEPTION", e)
        if ans:
            print("Found ans",ans)
            if confirm(CNF[k], ans):
                print("...checks out")
            else:
                print("NOPE")
        elif k not in ['easy', 'hard', 'easy_long']:
            print("...no answer checks out")
        else:
            print("NOPE: Couldn't find an answer for {}".format(k))
    
def test_randsat():
    for a in args:
        print("Trying n, k, m", a)
        try:
            cnf = randsat(*a)
        except Exception as e:
            print("...raised", e)
            continue
        print(cnf)
        m = len(cnf)
        n = get_max_lit(cnf)
        k = get_min_len(cnf)
        if n == a[0] and k == a[1] and m == a[2]:
            print("...result checks out")
        else:
            print("NOPE: {} got {}".format(a, (n, k, m)))


def random_sat_runner(n, k, m, num=10):
    """
    Generate num random sat problems
    Time satcom and satcomfast on them
    """
    print("Generating {} trials of {}".format(num, (n, k, m)))
    probs = [randsat(n, k, m) for _ in range(num)]
    
    def f1():
        for s in probs:
            satcom(s)
        
    def f2():
        for s in probs:
            satcom(s)
    t1 = timeit.timeit(f1, number=1)
    t2 = timeit.timeit(f2, number=1)
    print("SAT: {:5f} SATfast: {:5f} diff: {:5f}".format(t1, t2, t1-t2))


####### 8 PUZZLE - Question 2


def eight_runner(start, search):
    func = partial(search, start, SOLVED_EIGHT)
    if name == 'onem' or name == 'correct':
        n = 100
    elif name == 'easy' or 'short' in name:
        n = 10
    else:
        n = 1
    t = timeit.timeit(func, number=n)
    result = func()
    print(" {} T: {} L: {} R: {}".format(search.__name__, t, len(result), result))
   
   
def random_eight_runner(l=6, n=10):
    """
    Generate n random 8 puzzles of length (max) l
    Time ida and idas on them
    """
    print("Generating {} trials of length {} max".format(n, l))
    starts = [randep(l) for _ in range(n)]
    
    def f1():
        for s in starts:
            ids(s, SOLVED_EIGHT)
        
    def f2():
        for s in starts:
            idas(s, SOLVED_EIGHT)

    def f3():
        for s in starts:
            idasfast(s, SOLVED_EIGHT)

    t1 = timeit.timeit(f1, number=1)
    t2 = timeit.timeit(f2, number=1)
    t3 = timeit.timeit(f3, number=1)
    print("IDA: {:5f} IDA*: {:5f} diff: {:5f}".format(t1, t2, t1-t2))
    print("IDA*fast: {:5f} diff: {:5f}".format(t3, t3-t2))
    
    
if __name__ == "__main__":
    from sat_key import *
    print("Testing random SAT generator")
    test_randsat()
    
    print("Testing simple SAT problems")
    test_simple_sats(satcom)
    test_simple_sats(satcomfast)
    
    # some random ones
    random_sat_runner(5, 5, 5, num=100)
    # small difficult ones
    random_sat_runner(100, 2, 400, num=1)
    # big easy one
    random_sat_runner(n=100, k=3, m=200, num=1)
    # small difficult ones
    random_sat_runner(n=10, k=3, m=40, num=1)
    
    from eight_key import *
    for name, start in EIGHT.items():
        print("Testing {}".format(name))
        eight_runner(start, ids)
        eight_runner(start, idas)
        
    # some random short ones
    random_eight_runner(l=6, n=100)
    random_eight_runner(l=20)
    #random_runner(l=40, n=1)

                
                
