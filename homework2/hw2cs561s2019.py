from copy import deepcopy
from random import randint
from math import log
from time import time

def find_last(agg, limit):
    if not agg or agg[0][0] != 0:
        agg = [(0, 0)] + agg
    i = len(agg)-1
    while 0 <= i < len(agg) and agg[i][1] < limit:
        i -= 1
    return agg[i+1][0]

def count_helper(scheduled, L, start, end):
    # landing: lambda p: p[6]   lambda p: p[6]+p[2]
    # gating: lambda p: p[6]+p[2]     lambda p: p[7]
    # taking off: lambda p: p[7]    lambda p: p[7]+p[4]
    points = []
    for p in scheduled:
        points.append((start(p), 1))
        points.append((end(p), -1))
    points.sort()
    agg, count = [], 0
    for i in range(len(points)):
        count += points[i][1]
        if i == len(points)-1 or points[i][0] != points[i+1][0]:
            if count > L:
                return "invalid"
            agg.append((points[i][0], count))
    return agg

def valid(scheduled, L, G, T):
    l_counter = count_helper(scheduled, L, lambda p: p[6], lambda p: p[6]+p[2])
    g_counter = count_helper(scheduled, G, lambda p: p[6]+p[2], lambda p: p[7])
    t_counter = count_helper(scheduled, T, lambda p: p[7], lambda p: p[7]+p[4])
    if "invalid" in (l_counter, g_counter, t_counter):
        return False
    return True

def dfs(planes, scheduled, i, L, G, T):
    # complete case
    if len(scheduled) == len(planes):
        return True
    # pick a new plane
    p = planes[i]
    l_counter = count_helper(scheduled, L, lambda p: p[6], lambda p: p[6]+p[2])
    g_counter = count_helper(scheduled, G, lambda p: p[6]+p[2], lambda p: p[7])
    t_counter = count_helper(scheduled, T, lambda p: p[7], lambda p: p[7]+p[4])
    landing_after = find_last(l_counter, L)
    gating_after = max(0, find_last(g_counter, G) - p[2])
    takeoff_after = max(0, find_last(t_counter, T) - p[2] - p[5])
    safe_landing = max((landing_after, gating_after, takeoff_after))
    # add it to scheduled
    scheduled.append(p)
    # try first valid scheduling using greedy method(with some hueristic to speed up but may miss some solutions)
    for l_ in range(safe_landing, p[1]+1):
        p[6] = l_
        for at_gate in range(p[3], p[5]+1):
            p[7] = p[6] + p[2] + at_gate
            if valid(scheduled, L, G, T):
                break
        else:
            continue
        break
    # if the scheduling faild
    if not valid(scheduled, L, G, T):
        scheduled.pop()
        # switch the failed one with random previous plane, which means schedule it earlier next time
        j = randint(0, i)
        planes[i], planes[j] = planes[j], planes[i]
        return False
    if dfs(planes, scheduled, i+1, L, G, T):
        return True
    scheduled.pop()
    return False

if __name__ == '__main__':
    planes = []
    with open("input.txt") as read_f:
        L, G, T = map(int ,read_f.readline().strip().split(" "))
        N = int(read_f.readline().strip())
        planes = []
        for i in range(N):
            planes.append([i] + list(map(int, read_f.readline().split(" "))) + [-1,-1])
    planes.sort(key=lambda x: (x[1]+x[2], x[1]))
    heuristic_order = deepcopy(planes) # store original heuristic order
    res = []
    success = dfs(planes, res, 0, L, G, T)
    tried, cap = 1, max(100, N*log(N, 2))
    start_time = time()
    while not success:
        success = dfs(planes, res, 0, L, G, T)
        tried += 1
        print(tried, time()-start_time)
        if tried > cap:
            planes = deepcopy(heuristic_order) # roll back to original order
            tried = 0
    print(res)
    res.sort(key = lambda x: x[0])
    with open("output.txt", "w") as out_f:
        for p in res:
            out_f.write("{} {}\n".format(p[-2], p[-1]))