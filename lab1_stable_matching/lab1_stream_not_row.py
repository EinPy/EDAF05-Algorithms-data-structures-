import sys
from collections import *
sys.setrecursionlimit(10**5)
itr = (line for line in sys.stdin.read().strip().split('\n'))
INP = lambda: next(itr)
def ni(): return int(INP()) # new int
def nl(): return [int(_) for _ in INP().split()] #new line of ints


def check_pref(comp, s1, s2):
    for c in comp:
        if c == s2:
            return True
        if c == s1:
            return False
        
def check_pref_fast(comp, s1, s2, company_ranking):
    if company_ranking[comp][s2] < company_ranking[comp][s1]:
        return True
    else:
        return False


def solve(pairs, company, student, q, company_ranking):

    q = deque(q)
    applicants = [-1 for _ in range(pairs+1)]
    
    while q:
        s = q.popleft()
        #print(student)
        ranking,  apply_idx = student[s]
        pref_comp = ranking[apply_idx]

        curr_applicant = applicants[pref_comp]
        #no previous applicants
        if applicants[pref_comp] == -1:
            applicants[pref_comp] = s

        elif check_pref_fast(pref_comp, curr_applicant, s, company_ranking):
            q.append(applicants[pref_comp])
            applicants[pref_comp] = s

        else:
            q.append(s)
        student[s][1] += 1

    print('\n'.join(map(str,applicants[1:])))



pairs = ni()
#note that problem is 1 idexed
#using array as they are faster than dict
#structure arr[id] = [[preferences], current application id]
company = [[] for _ in range(pairs+1)]
student = [[]for _ in range(pairs+1)]
company_ranking = [[1e5 for i in range(pairs+1)] for i in range(pairs+1)] #more memory for better time complexiity? O(N^2) memory
student_ids = []

seen = {}


#really a low blow to not format in rows
inputstream = []
while True:
    try:
        inputstream += nl() #Isslow
    except:
        break

# 
for block in range(2*pairs):
    row = []
    if block == 0:
        idx = 0
        row = inputstream[1:pairs+1]
    else:
        idx = (pairs+1)*block
        row = inputstream[(pairs+1)*block+1:(pairs+1)*block + pairs+1] #this is also slow, slicing list = bad
    id = inputstream[idx]
    if id in seen:
        student[id] = [row, 0]
        student_ids.append(id)
    else:
        company[id] = row
        seen[id] = True
        for i in range(len(company[id])): #O(N^2)
            company_ranking[id][company[id][i]] = i
    
# for row in company_ranking:
#     print(row)



solve(pairs,company, student, student_ids, company_ranking)