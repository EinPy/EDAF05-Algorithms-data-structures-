import sys
from collections import *
sys.setrecursionlimit(10**5)
itr = (line for line in sys.stdin.read().strip().split('\n'))
INP = lambda: next(itr)
def ni(): return int(INP())
def nl(): return [int(_) for _ in INP().split()]

gamma = -4


def printg(graph):
    for l in graph:
        print(l)

def solve(a,b, pos, cost):
    na = len(a)
    nb = len(b)
    dp = [[0 for _ in range(nb+1)] for _ in range(na+1)]


    best = 0
    br, bc = 0, 0
    #index 0 aligned with 0
    # ia0 = pos[a[0]]
    # ib0 = pos[b[0]]
    # score = costs[ia0][ib0]
    # dp[0][0] = score[ia0][ib0]

    # best = max(best, dp[0][0])
    #pre allocate index 0, row and col
    for r in range(1,na+1):
        dp[r][0] += dp[r-1][0] + gamma

    for c in range(1, nb+1):
        dp[0][c] += dp[0][c-1] + gamma

    #printg(dp)

    for r in range(1, na+1):
        for c in range(1, nb + 1):
            ia = pos[a[r-1]]
            ib = pos[b[c-1]]
            score = cost[ia][ib]
            dp[r][c] = max(dp[r-1][c-1] + score, dp[r-1][c] + gamma, dp[r][c-1] + gamma)
            if dp[r][c] > best:
                best = dp[r][c]
                br, bc = r, c
    #printg(dp)
    #backtracking to construct strings
    #string slicing expensive so use lists?
    r = na 
    c = nb 
    align_a = []
    align_b = []
    while r > 0 or c > 0:
        if r > 0 and c > 0 and dp[r][c] == dp[r-1][c-1] + cost[pos[a[r-1]]][pos[b[c-1]]]:
            align_a.append(a[r-1])
            align_b.append(b[c-1])
            r -= 1
            c -= 1
        elif r > 0 and dp[r][c] == dp[r-1][c] + gamma:
            align_a.append(a[r-1])
            align_b.append('*')
            r -= 1
        elif c > 0 and dp[r][c] == dp[r][c-1] + gamma:
            align_a.append('*')
            align_b.append(b[c-1])
            c -= 1

    align_a.reverse()
    align_b.reverse()
    print(''.join(align_a), ''.join(align_b))
 

letters = INP().split()
#find index of letter in string
pos = {}
for i in range(len(letters)):
    pos[letters[i]] = i

lines = len(letters)
costs = []
for l in range(lines):
    arr = nl()
    costs.append(arr)
queries = ni()
for l in range(queries):
    a,b = INP().split()
    solve(a,b, pos, costs)


#solution is iterative
#the time complexity is O(N*M) where N and M are the lengths of the words
#recursive solutions without cache(=memoization?) would be really bad
#3 choices for each, insert a, insert b and keep?
#branching factor 3, depth N+M, O(3^(N+M))
#bioinformatics, aligning dna sequences,
#score represent how difficult it is to align diffrent things