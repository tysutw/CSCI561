from time import time
TIME_OUT_LIMIT = 28.0

class CashMiner(object):
    def __init__(self, N, walls, terminals, p, Rp, gamma):
        self.n = N
        self.grid = [[0.0]*N for _ in xrange(N)]
        self.walls = walls
        self.terminals = terminals
        self.p = p
        self.dp = (1.0-p)/2
        self.gamma = gamma
        self.round = 0
        self.Rp = Rp
        for i in xrange(self.n):
            for j in xrange(self.n):
                if (i, j) not in walls and (i,j) not in terminals:
                    self.grid[i][j] = Rp
                elif (i, j) in self.terminals:
                    self.grid[i][j] = self.terminals[(i, j)]

    def iterate(self):
        start_time = time()
        change = True
        while change and time()-start_time < TIME_OUT_LIMIT:
            new_grid = [[0.0]*N for _ in xrange(N)]
            change = False
            for i in xrange(self.n):
                for j in xrange(self.n):
                    if (i, j) in self.walls:
                        continue
                    elif (i, j) in self.terminals:
                        new_grid[i][j] = self.grid[i][j]
                        continue
                    val, _ = self.get_best_action(i, j)
                    new_grid[i][j] = self.Rp + self.gamma * val
                    if abs(new_grid[i][j] - self.grid[i][j]) > 0.001:
                        change = True
            self.grid = new_grid

    def print_policy(self):
        with open("output.txt","w") as output_f:
            for i in xrange(self.n):
                line = [self.get_best_action(i, j)[1] for j in xrange(self.n)]
                for j in xrange(self.n):
                    if (i, j) in self.walls:
                        line[j] = 'N'
                    if (i, j) in self.terminals:
                        line[j] = 'E'
                output_f.write(",".join(line))
                output_f.write("\n")

    def get_best_action(self, i, j):
        best_util = float('-inf')
        best_dir = '_'
        for dx, dy, vertical, direction in [(1,0,True,"D"),(-1,0,True,"U"),(0,1,False,"R"),(0,-1, False,"L")]:
            expected_util = self.get_util(i+dx, j+dy, vertical, self.grid[i][j])
            if expected_util > best_util:
                best_util = expected_util
                best_dir = direction
        return best_util, best_dir

    def get_util(self, i, j, vertical, org_util):
        total_util = self.p*self.grid[i][j] if self.valid_pos(i, j) else self.p*org_util
        if vertical:
            for d in [-1,1]:
                if self.valid_pos(i, j+d):
                    total_util += self.dp*self.grid[i][j+d]
                else:
                    total_util += self.dp*org_util
        else:
            for d in [-1,1]:
                if self.valid_pos(i+d, j):
                    total_util += self.dp*self.grid[i+d][j]
                else:
                    total_util += self.dp*org_util
        return total_util

    def valid_pos(self, x, y):
        return (x,y) not in self.walls and 0 <= x < self.n and 0 <= y < self.n

if __name__ == '__main__':
    with open("input.txt") as input_f:
        
        N = int(input_f.readline().strip())
        num_walls = int(input_f.readline().strip())
        walls, terminals = set(), {}
        
        for _ in xrange(num_walls):
            x, y = input_f.readline().strip().split(",")
            walls.add((int(x)-1, int(y)-1))
        
        num_terminals = int(input_f.readline().strip())

        for _ in xrange(num_terminals):
            x, y, v = input_f.readline().strip().split(",")
            terminals[(int(x)-1, int(y)-1)] = float(v)
        
        P = float(input_f.readline().strip())
        Rp = float(input_f.readline().strip())
        gamma = float(input_f.readline().strip())
        
        cm = CashMiner(N, walls, terminals, P, Rp, gamma)
        cm.iterate()
        cm.print_policy()