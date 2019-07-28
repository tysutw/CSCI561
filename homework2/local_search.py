from random import randint
from copy import deepcopy
from math import sqrt
import signal

def loss(planes, l_t, L, start, end):
    # landing: lambda p: p[6]   lambda p: p[6]+p[2]
    # gating: lambda p: p[6]+p[2]     lambda p: p[7]
    # taking off: lambda p: p[7]    lambda p: p[7]+p[4]
    points = []
    for i in range(len(l_t)):
        points.append((start(planes[i], l_t[i]), 1))
        points.append((end(planes[i], l_t[i]), -1))
    points.sort()
    agg, count = [], 0
    for i in range(len(points)):
        count += points[i][1]
        if i == len(points)-1 or points[i][0] != points[i+1][0]:
            agg.append((points[i][0], count))
    # print(agg)
    loss = 0
    for i in range(len(agg)-1):
        if agg[i][1] > L:
            loss += (agg[i][1]-L) * (agg[i+1][0] - agg[i][0])
    return loss

def get_score(planes, schedule, L, G, T):
    total = 0
    total += loss(planes, schedule, L, lambda x,y: y[0], lambda x,y: y[0]+x[1])
    total += loss(planes, schedule, G, lambda x,y: y[0]+x[1], lambda x,y: y[1])
    total += loss(planes, schedule, T, lambda x,y: y[1], lambda x,y: y[1]+x[3])
    return total

planes = []

with open("input.txt") as read_f:

    L, G, T = map(int ,read_f.readline().strip().split(" "))
    
    N = int(read_f.readline().strip())

    for i in range(N):
        raw = list(map(int, read_f.readline().split(" ")))
        '''
        R M S O C l t
        0 1 2 3 4 5 6
        '''
        planes.append(raw + [-1, -1])
    
schedules = []
min_score = 9999999
while len(schedules) < N:
    schedule = []
    for p in planes:
        landing = randint(0, p[0])
        takeoff = landing + randint(p[2], p[4])
        schedule.append((landing, takeoff))
    score = get_score(planes, schedule, L, G, T)
    min_score = min(min_score, score)
    print(min_score)
    if score < 100:
        schedules.append(schedule)
    
scores_schedules = [(get_score(planes, schedule, L, G, T), schedule) for schedule in schedules]
scores_schedules.sort()

round = 0

while scores_schedules[0][0] != 0:
    nxt = []
    for score, schedule in scores_schedules:
        for _ in range(int(sqrt(N))):
            i = randint(0, N-1)
            for dl, dt in ((1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)):
                newlanding = schedule[i][0] + dl
                newtakeoff = schedule[i][1] + dt
                if 0 <= newlanding <= planes[i][0] and planes[i][2] <= (newtakeoff-newlanding)-planes[i][1] <= planes[i][4]:
                    tmp = deepcopy(schedule)
                    tmp[i] = (newlanding, newtakeoff)  
                    nxt.append(tmp)
    scores_schedules = sorted([(get_score(planes, schedule, L, G, T), schedule) for schedule in nxt])[:N]
    round += 1
    print(round, scores_schedules[0][0])
    
print(scores_schedules)
print(scores_schedules[0][1])

