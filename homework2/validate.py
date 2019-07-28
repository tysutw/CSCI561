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
                return("invalid")
            agg.append((points[i][0], count))
    return agg

scheduled = [[26, 10, 75, 60, 80, 80, 0, 135], [11, 49, 13, 27, 58, 147, 0, 40], [25, 15, 30, 65, 70, 65, 0, 95], [15, 59, 9, 59, 27, 179, 0, 68], [10, 7, 59, 89, 59, 209, 0, 148], [16, 45, 12, 115, 49, 235, 0, 127], [21, 13, 5, 85, 8, 205, 9, 99], [6, 50, 15, 5, 21, 125, 12, 32], [27, 50, 15, 10, 15, 80, 13, 38], [8, 68, 5, 31, 51, 151, 14, 50], [7, 41, 2, 107, 59, 227, 19, 128], [0, 30, 54, 33, 56, 153, 21, 108], [28, 65, 40, 65, 70, 75, 49, 164], [20, 32, 56, 82, 36, 202, 27, 165], [22, 72, 10, 45, 59, 165, 28, 83], [19, 41, 58, 91, 37, 211, 30, 179], [13, 75, 4, 91, 25, 211, 59, 187], [3, 76, 43, 84, 13, 204, 63, 201], [18, 85, 18, 77, 26, 197, 75, 207], [9, 86, 16, 38, 38, 158, 75, 212], [2, 100, 13, 8, 21, 128, 83, 104], [1, 103, 33, 23, 13, 143, 88, 214], [12, 107, 31, 72, 4, 192, 89, 215], [24, 120, 21, 36, 25, 156, 106, 216], [23, 98, 50, 76, 58, 196, 91, 219], [17, 120, 46, 85, 11, 205, 93, 227], [5, 140, 40, 111, 29, 231, 108, 259], [14, 155, 30, 74, 48, 194, 134, 238], [4, 163, 22, 72, 2, 192, 143, 237]]

l_counter = count_helper(scheduled, 6, lambda p: p[6], lambda p: p[6]+p[2])
g_counter = count_helper(scheduled, 13, lambda p: p[6]+p[2], lambda p: p[7])
t_counter = count_helper(scheduled, 6, lambda p: p[7], lambda p: p[7]+p[4])

print(l_counter, g_counter, t_counter)