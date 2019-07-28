'''
format
i R M S O C l t
0 1 2 3 4 5 6 7
'''
from copy import deepcopy
from time import time

from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,seconds) #used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator

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

def dfs(remaining, scheduled):
    l_counter = count_helper(scheduled, L, lambda p: p[6], lambda p: p[6]+p[2])
    g_counter = count_helper(scheduled, G, lambda p: p[6]+p[2], lambda p: p[7])
    t_counter = count_helper(scheduled, T, lambda p: p[7], lambda p: p[7]+p[4])

    if "invalid" in (l_counter, g_counter, t_counter):
        return False
    
    if not remaining:
        return True
    
    # try all next from candicates in heuristic order
    for i in range(len(remaining)):
        p = remaining[i]
        landing_after = find_last(l_counter, L)
        gating_after = max(0, find_last(g_counter, G) - p[2])
        takeoff_after = max(0, find_last(t_counter, T) - p[2] - p[5])
        safe_landing = max((landing_after, gating_after, takeoff_after))
        # if greedy aproach does not work, exhaustively try domain from raw input
        landing_domain = range(p[1]) if safe_landing > p[1] else range(safe_landing, p[1])
        for l_ in landing_domain:
            p[6] = l_
            scheduled.append(p)
            for at_gate in range(p[3], p[5]+1):
                p[7] = safe_landing + p[2] + at_gate
                if dfs(remaining[:i] + remaining[i+1:], scheduled):
                    return True
            scheduled.pop()
        print([x[0] for x in scheduled])
    return False

@timeout(1)
def execute(planes, res):
    success = dfs(planes, res)
    
if __name__ == '__main__':

    planes = []
    with open("input.txt") as read_f:

        L, G, T = map(int ,read_f.readline().strip().split(" "))
        N = int(read_f.readline().strip())
        planes = []
        for i in range(N):
            planes.append([i] + list(map(int, read_f.readline().split(" "))) + [-1,-1])

    planes.sort(key=lambda x: (x[1]+x[2], x[1]))
    try:
        begin = time()
        res = []
        success = dfs(deepcopy(planes), res)
    except TimeoutError as e:
        print("Time elapsed: {:.3f}s".format(time() - begin))
    res.sort(key = lambda x: x[0])

    with open("output.txt", "w") as out_f:
        for p in res:
            out_f.write("{} {}\n".format(p[-2], p[-1]))
