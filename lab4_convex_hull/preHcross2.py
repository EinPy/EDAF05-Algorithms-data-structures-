import sys
from collections import *
sys.setrecursionlimit(10**5)
itr = (line for line in sys.stdin.read().strip().split('\n'))
INP = lambda: next(itr)
def ni(): return int(INP())
def nl(): return [int(_) for _ in INP().split()]

def cross_product(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def is_left_turn(p, q, r):
    return cross_product(p, q, r) > 0

def is_rigth_turn(p, q, r):
    return cross_product(p, q, r) < 0

def is_colinear(p,q,r):
    return cross_product(p,q,r) == 0

def rm_colin(points):
    include = [True for _ in range(len(points))]
    for i in range(1, len(points)-1):
        if is_colinear(points[i-1], points[i], points[i+1]):
            include[i] = False
    new = []
    for i in range(len(include)):
        if include[i]:
            new.append(points[i])
    return new

def convex_hull_base_case(points):
    if len(points) < 2:
        return points
    elif len(points) == 2:
        return points if points[0][0] <= points[1][0] else [points[1], points[0]]
    elif len(points) == 3:
        if cross_product(points[0], points[1], points[2]) == 0:
            tmp = sorted(points, key=lambda x: (x[0], x[1]))
            return [tmp[0], tmp[2]]
        else:
            rightmost = max(points, key=lambda x: (x[0], -x[1]))
            points.pop(points.index(rightmost))
            topmost = max(points, key=lambda x: x[1])
            points.pop(points.index(topmost))
            bottommost = points[0]

            out1 = [rightmost, bottommost, topmost]
            out2 = [rightmost, topmost, bottommost]
            if not is_left_turn(rightmost, bottommost, topmost):
                return out1
            else:
                return out2

def merge_hulls(left_hull, right_hull):
    n_left = len(left_hull)
    n_right = len(right_hull)


    lh_rightmost_top = left_hull.index(max(left_hull, key=lambda p: p[0]))
    lh_righmost_bot = lh_rightmost_top
    rh_leftmost_top = right_hull.index(min(right_hull, key=lambda p: p[0]))
    rh_leftmost_bot = rh_leftmost_top
    #print("left part: ", left_hull[lh_rightmost_top])
    #print("right parth: ", right_hull[rh_leftmost_bot])

    if n_left == 1:
        #find the starting and endpoint of the right hull
        while True:
            changed = False
            #right hull sorted in clockwise order, should move forward in list,
            #upper tangent can always be found
            while (is_left_turn(left_hull[0],right_hull[rh_leftmost_top], right_hull[(rh_leftmost_top+1)%n_right])
                or is_colinear(left_hull[0],right_hull[rh_leftmost_top], right_hull[(rh_leftmost_top+1)%n_right])):
                rh_leftmost_top = (rh_leftmost_top + 1) % n_right
                changed = True

            if not changed: #points should have created upper tangent for both hulls
                break
        while True:
            changed = False

            #right hull sorted in clockwise order, should move backwards in list
            #lower tangent can alwyas be found 
            while (is_rigth_turn(left_hull[0], right_hull[rh_leftmost_bot], right_hull[rh_leftmost_bot-1])
                or is_colinear(left_hull[0], right_hull[rh_leftmost_bot], right_hull[rh_leftmost_bot-1])):
                rh_leftmost_bot = (rh_leftmost_bot - 1) % n_right
                changed = True
            if not changed:
                break

    elif n_right == 1:
        while True:
            changed = False
            #since left is sorted in clockwise order, should move backwards in list
            #upper tangent can always be found
            while (is_rigth_turn(right_hull[0], left_hull[lh_rightmost_top], left_hull[lh_rightmost_top -1])  
                or is_colinear(right_hull[0], left_hull[lh_rightmost_top], left_hull[lh_rightmost_top -1])):
                lh_rightmost_top = (lh_rightmost_top - 1) % n_left
                changed = True

            if not changed: #points should have created upper tangent for both hulls
                break

        #repeat process for bottom points
        while True:
            changed = False
            #left sorted in clockwise order, should move forwards in list
            while (is_left_turn(right_hull[0], left_hull[lh_righmost_bot], left_hull[(lh_righmost_bot+1)%n_left])
                    or is_colinear(right_hull[0], left_hull[lh_righmost_bot], left_hull[(lh_righmost_bot+1)%n_left])):
                lh_righmost_bot = (lh_righmost_bot + 1) % n_left
                changed = True

            if not changed:
                break
    
    else:
        #start by checking if the lh point can be moved upwards to create an upper tanget
        #then check if the rh point can be moved upwards to create upper tangent
        #repeat until the line is an upper tangent for both hulls

        #do the same but move down instead. 
        #check if above or below line, all convex hulls encounterd should be sorted in clockwise order. 
        visL, visR = 1, 1
        while True:
            changed = False

            #since left is sorted in clockwise order, should move backwards in list
            #upper tangent can always be found
            while (is_rigth_turn(right_hull[rh_leftmost_top], left_hull[lh_rightmost_top], left_hull[lh_rightmost_top -1])  
                or is_colinear(right_hull[rh_leftmost_top], left_hull[lh_rightmost_top], left_hull[lh_rightmost_top -1])
                and visL + 1 <= n_left):
                #print("right turn")
                lh_rightmost_top = (lh_rightmost_top - 1) % n_left
                changed = True
                visL += 1

                
            #right hull sorted in clockwise order, should move forward in list,
            #upper tangent can always be found
            while (is_left_turn(left_hull[lh_rightmost_top],right_hull[rh_leftmost_top], right_hull[(rh_leftmost_top+1)%n_right])
                or is_colinear(left_hull[lh_rightmost_top],right_hull[rh_leftmost_top], right_hull[(rh_leftmost_top+1)%n_right])
                and visR +1 <= n_right):
                #print("left turn")
                rh_leftmost_top = (rh_leftmost_top + 1) % n_right
                changed = True
                visR += 1

            if not changed: #points should have created upper tangent for both hulls
                break
        #print("top left is: ", left_hull[lh_rightmost_top])
        #print("top right is: ", right_hull[rh_leftmost_top]) # seems right

        #repeat process for bottom points
        visL, visR = 1, 1
        while True:
            changed = False
            #left sorted in clockwise order, should move forwards in list
            while (is_left_turn(right_hull[rh_leftmost_bot], left_hull[lh_righmost_bot], left_hull[(lh_righmost_bot+1)%n_left])
                    or is_colinear(right_hull[rh_leftmost_bot], left_hull[lh_righmost_bot], left_hull[(lh_righmost_bot+1)%n_left])
                    and visL + 1 <= n_left):
                lh_righmost_bot = (lh_righmost_bot + 1) % n_left
                changed = True
                visL +=1
            #right hull sorted in clockwise order, should move backwards in list
            #lower tangent can alwyas be found 
            while (is_rigth_turn(left_hull[lh_righmost_bot], right_hull[rh_leftmost_bot], right_hull[rh_leftmost_bot-1])
                or is_colinear(left_hull[lh_righmost_bot], right_hull[rh_leftmost_bot], right_hull[rh_leftmost_bot-1])
                and visR + 1 <= n_right):
                rh_leftmost_bot = (rh_leftmost_bot - 1) % n_right
                changed = True
                visR += 1
            if not changed:
                break
        #print("bot left is: ", left_hull[lh_righmost_bot])
        #print("bot right is: ", right_hull[rh_leftmost_bot]) # seems right

    #slicing lists cleverly should be able to preserve clockwise order
    # uneccecary to fix right bot point first, that can be afterprocessed, but 
    #clockwise is essential
    out = []

    #fix left half
    idx = lh_righmost_bot
    if lh_righmost_bot == lh_rightmost_top:
        out.append(left_hull[idx])
    else:
        while idx != lh_rightmost_top:
            out.append(left_hull[idx])
            idx = (idx + 1) % n_left
        out.append(left_hull[idx])

    #fix right half
    idx = rh_leftmost_top
    if rh_leftmost_top == rh_leftmost_bot:
        out.append(right_hull[idx])
    else:
        while idx != rh_leftmost_bot:
            out.append(right_hull[idx])
            idx = (idx + 1) % n_right
        out.append(right_hull[idx])

    return rm_colin(out)
    





def split_points(points):
    n = len(points)
    mid = n // 2
    left_hull = points[:mid]
    right_hull = points[mid:]

    # Check if any points have the same x coordinate as the last point in the left hull
    while len(right_hull) > 0 and right_hull[0][0] == left_hull[-1][0]:
        left_hull.append(right_hull.pop(0)) # slow but I don't care anymore, could import deque and use leftpop

    return left_hull, right_hull

def preparata_hong(points):
    
    if len(points) <= 3:
        #print(points)
        return convex_hull_base_case(points)

    lh, rh = split_points(points)
    # print(lh)
    # print(rh)
    left_hull = preparata_hong(lh)
    right_hull = preparata_hong(rh)
    
    #print(left_hull)
    #print(right_hull)
    return merge_hulls(left_hull, right_hull)


# points = [(1, 1), (2, 2), (3, 1), (2, 3), (1, 5), (3, 5), (5, 5), (6, 3), (7, 1)]
# sorted_points = sorted(points, key=lambda x: (x[0], x[1]))
# convex_hull = preparata_hong(sorted_points)
# print(convex_hull)

dim, num_p = nl()
points = []
allInt = True
for line in range(num_p):
    hexx, hexy, hashtg, fx, fy = INP().split()
    x = float(fx)
    y = float(fy)
    if x != round(x) or y != round(y):
        allInt = False
    points.append([x, y])
#print(points)
sorted_points = sorted(points, key=lambda x: (x[0], x[1]))
sorted_points = rm_colin(sorted_points)
#print(sorted_points)
cnvx_hll = preparata_hong(sorted_points)
#print(cnvx_hll)

#assume code is correct in clockwise order, find rightmost point
rr = -10**10
tt = -10**10
idx = 0
for i in range(len
               (cnvx_hll)):
    if cnvx_hll[i][0] >rr or (cnvx_hll[i][0] == rr and cnvx_hll[i][1] > tt):
        rr = cnvx_hll[i][0]
        tt = cnvx_hll[i][1]
        idx = i
ordered = cnvx_hll[idx:] + cnvx_hll[:idx]

print(len(ordered))
for x,y in ordered:
    if allInt: print(int(x), int(y))
    else: print(f"{x:.3f} {y:.3f}")