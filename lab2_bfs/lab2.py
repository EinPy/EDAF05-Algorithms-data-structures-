import sys
from collections import *
sys.setrecursionlimit(10**5)
itr = (line for line in sys.stdin.read().strip().split('\n'))
INP = lambda: next(itr)
def ni(): return int(INP())
def nl(): return [int(_) for _ in INP().split()]


N, Q = nl()
words = []
posInAdj = {}
#O(N^2) to create graph?
cnt = []
adj = [[] for _ in range(N)]

#Bfs to find distannce to all nodes in graph 
#If Q > N faster with floyd warshall??
def bfs(start, finish):
    if start == finish:
        return 0
    q = deque([start])
    dists = [-1 for _ in range(len(adj))]
    dists[start] = 0
    while q:
        q2 = []
        for u in q:
            for n in adj[u]:
                if dists[n] == -1:
                    dists[n] = dists[u] + 1
                    q2.append(n)
                    if n == finish:
                        return dists[n]
        q = q2
    return -1




for line in range(N):
    w = INP()
    words.append(w)
    cnt.append(Counter(w))
    posInAdj[w] = line

#create adjecency list in O(N^2)
for i in range(N):
    fr = Counter(words[i][-4:])
    #print(words[i], words[i][-4:])
    for j in range(N):
        if j != i:
            match = True
            for k in fr.keys():
                if cnt[j][k] < fr[k]:
                    match = False
                    break
            if match:
                adj[i].append(j)

out = []
#print(adj)

for line in range(Q):
    a, b = INP().split(" ")
    ans = bfs(posInAdj[a], posInAdj[b])
    if ans == -1:
        out.append("Impossible")
    else:
        out.append(ans)

print("\n".join(map(str,out)))