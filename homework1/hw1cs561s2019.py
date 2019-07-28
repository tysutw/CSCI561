from copy import deepcopy

class MinMax:
    def __init__(self, n, d_limit = 4):
        self.n = n
        self.dirs = [[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]]
        self.limit = d_limit

    def alpha_beta_search(self, grid):
        self.preprocess(grid)
        candidates = self.get_candidates(grid)
        if not candidates:
            return self.score(grid)
        alpha, beta = float('-inf'), float('inf')
        v, x, y = float('-inf'), -1, -1
        for i, j in candidates:
            new_grid = deepcopy(grid)
            self.put(new_grid, i, j, 1)
            t = self.min_value(new_grid, alpha, beta, 1)
            if t > v:
                v, x, y = t, i, j
            if v >= beta:
                return x, y
            alpha = max(alpha, v)
        return x, y
    
    def max_value(self, grid, alpha, beta, d):
        if d >= self.limit:
            return self.score(grid)
        candidates = self.get_candidates(grid)
        if not candidates:
            return self.score(grid)
        v = float('-inf')
        for i, j in candidates:
            new_grid = deepcopy(grid)
            self.put(new_grid, i, j, 1)
            v = max(v, self.min_value(new_grid, alpha, beta, d+1))
            if v>= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, grid, alpha, beta, d):
        if d >= self.limit:
            return self.score(grid)
        candidates = self.get_candidates(grid)
        if not candidates:
            return self.score(grid)
        v = float('inf')
        for i, j in candidates:
            new_grid = deepcopy(grid)
            self.put(new_grid, i, j, 2)
            v = min(v, self.min_value(new_grid, alpha, beta, d+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def get_candidates(self, grid):
        res = []
        for i in xrange(self.n):
            for j in xrange(self.n):
                if grid[i][j] == 0:
                    res.append((i, j))
        return res

    def score(self, grid):
        score = 0
        for i in xrange(self.n):
            for j in xrange(self.n):
                cell = grid[i][j]
                if cell == 1 or cell == 4:
                    score += 1
                elif cell == 2 or cell == 5:
                    score -= 1
        return score
    
    def put(self, grid, i, j, p):
        grid[i][j] = p
        for dx, dy in self.dirs:
            x, y = i+dx, j+dy
            if x < 0 or y < 0 or x >= n or y >= n or grid[x][y] == 3:
                continue
            if grid[x][y] == 0:
                if p == 1:
                    grid[x][y] = 4
                elif p == 2:
                    grid[x][y] = 5
            elif (grid[x][y] == 4 and p == 2) or (grid[x][y] == 5 and p == 1):
                grid[x][y] = 6
            x += dx
            y += dy
            if x < 0 or y < 0 or x >= n or y >= n or grid[x][y] == 3:
                continue
            if grid[x][y] == 0:
                if p == 1:
                    grid[x][y] = 4
                elif p == 2:
                    grid[x][y] = 5
            elif (grid[x][y] == 4 and p == 2) or (grid[x][y] == 5 and p == 1):
                grid[x][y] = 6
    
    def preprocess(self, grid):
        for i in xrange(self.n):
            for j in xrange(self.n):
                if grid[i][j] == 1 or grid[i][j] == 2:
                    self.put(grid, i, j, grid[i][j])
        
if __name__ == '__main__':
    n = 0
    grid = []
    with open('input.txt', 'r') as input_file:
        n = int(input_file.readline())
        for _ in range(n):
            grid.append([int(c) for c in input_file.readline() if c.isdigit()])
    mm = MinMax(n)
    x, y = mm.alpha_beta_search(grid)
    with open('output.txt', 'w') as output_file:
        output_file.write('{} {}'.format(x, y))
    