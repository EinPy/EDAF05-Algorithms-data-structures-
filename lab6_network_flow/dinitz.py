import sys
from collections import defaultdict
import copy
sys.setrecursionlimit(10**5)
itr = (line for line in sys.stdin.read().strip().split('\n'))
INP = lambda: next(itr)
def ni(): return int(INP())
def nl(): return [int(_) for _ in INP().split()]






class Dinitz:
    def __init__(self, sz, INF=10**10):
        self.G = [defaultdict(int) for _ in range(sz)]
        self.sz = sz
        self.INF = INF

    def add_edge(self, i, j, w):
        self.G[i][j] += w

    def bfs(self, s, t):
        level = [0]*self.sz
        q = [s]
        level[s] = 1
        while q:
            q2 = []
            for u in q:
                for v, w in self.G[u].items():
                    if w and level[v] == 0:
                        level[v] = level[u] + 1
                        q2.append(v)
            q = q2
        self.level = level
        return level[t] != 0

    def dfs(self, s, t, FLOW):
        if s in self.dead: return 0
        if s == t: return FLOW

        for idx in range(self.pos[s], len(self.adj[s])):
            u = self.adj[s][idx]
            w = self.G[s][u]
            F = self.dfs(u, t, min(FLOW, w))
            if F:
                self.G[s][u] -= F
                self.G[u][s] += F
                if self.G[s][u] == 0:
                    self.pos[s] = idx+1
                    if idx + 1 == len(self.adj[s]):
                        self.dead.add(s)
                return F
            self.pos[s] = idx+1
        self.dead.add(s)
        return 0

    def setup_after_bfs(self):
        self.adj = [[v for v, w in self.G[u].items() if w and self.level[u] + 1 == self.level[v]] for u in range(self.sz)]
        self.pos = [0]*self.sz
        self.dead = set()
    def max_flow(self, s, t):
        flow = 0
        while self.bfs(s, t):
            self.setup_after_bfs()
            while True:
                pushed = self.dfs(s, t, self.INF)
                if not pushed: break
                flow += pushed
        return flow
    
    def printNice(self):
        for dict in self.G:
            print(dict)
        print()

    

nodes, edgeCount, student, routes = nl()
edges = []
remove= []
graph = Dinitz(nodes)
for line in range(edgeCount):
    u, v, w = nl()
    graph.add_edge(u,v,w)
    graph.add_edge(v,u,w)
    edges.append((u,v, w))

for line in range(routes):
    remove.append(ni())



#function is monotone, can binary search it?

def ok(remCnt):
    nexG = Dinitz(0)
    nexG.sz = nodes
    nexG.G = copy.deepcopy(graph.G)
    #graph[u][v] = #org cap
    for i in range(remCnt):
        u, v, w = edges[remove[i]]
        nexG.G[u][v] -= w
        nexG.G[v][u] -= w
    ans = nexG.max_flow(0, nodes-1)
    return ans >= student, ans
    

#Binary search for higher bound
def lower_bound():
    l, r, m = 0, routes, 0
    idx = -1
    cnt = 0
    while l <= r:
        mid = (l + r) // 2
        isValid, tmp = ok(mid)
        if isValid:
            idx = mid
            cnt = tmp
            l = mid + 1
        else:
            r = mid -1
    return idx, cnt

r, flow = lower_bound()
print(r, flow)

#Dinitz (wrong), O(VE^2)