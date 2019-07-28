from random import randint

res = []

for i in range(50):
    a = [i] + [0]*7
    cur = 0
    cur += randint(0, 50)
    a[-2]
    cur += randint(0, 100)
    a[-1] = cur
    a[1] = a[-2] + randint(0, 20)
    l2t = a[-1] - a[-2]
    a[2] = randint(l2t) #
    a[3] = randint(l2t-a[2])
    a[4] = randint(30)
    a[5] = randint()

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

l_counter = count_helper(scheduled, L, lambda p: p[6], lambda p: p[6]+p[2])
g_counter = count_helper(scheduled, G, lambda p: p[6]+p[2], lambda p: p[7])
t_counter = count_helper(scheduled, T, lambda p: p[7], lambda p: p[7]+p[4])