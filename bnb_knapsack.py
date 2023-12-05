import numpy as np

class BnB_knapsack:
    def __init__(self, W, v, w):
        self.W = W
        self.v = v
        self.w = w
        self.n = len(w)
        self.n_ori = len(w)
        self.M = None
        self.z_best = None
        self.x_best = None
        self.m = None
        self.U = None
        self.N = None

    def calculate_upper_bound(self, W_1, V_N, i):
        if i + 2 >= self.n:
            return V_N
        z_1 =  V_N + (W_1/self.w[i+1]) * self.v[i+1]
        W_2 = W_1 - (W_1/self.w[i+1]) * self.v[i+1]
        U_1 = z_1 + np.floor(W_2 * (self.v[i+2] / self.w[i+2]))
        U_2 = z_1 + np.floor(((W_2 + np.ceil((1 / self.w[i]) * (self.w[i+1] - W_2)) * self.w[i]) * self.v[i+2] / self.w[i+1]) - np.ceil((1 / self.w[i]) * (self.w[i+1] - W_2)) * self.v[i])
        return max(U_1, U_2)

    def eliminate_dominated_items(self):
        N = list(range(self.n))
        j = 0
        while j < len(N) - 1:
            k = j + 1
            while k < len(N):
                if self.w[N[k]] // self.w[N[j]] * self.v[N[j]] >= self.v[N[k]]:
                    N.pop(k)
                elif self.w[N[j]] // self.w[N[k]] * self.v[N[k]] >= self.v[N[j]]:
                    N.pop(j)
                    k = len(N)  # Break inner loop
                else:
                    k += 1
            j += 1

        N = sorted(N, key=lambda i: self.v[i] / self.w[i], reverse=True)
        self.N = N
        self.w = [self.w[i] for i in N]
        self.v = [self.v[i] for i in N]
        self.n = len(N)

    def initialize(self):
        # print("init")
        self.z_best = 0
        self.x_best = [0] * self.n
        x = [0] * self.n
        i = 0

        self.M = np.zeros((self.n, self.W+1))

        x[0] = self.W//self.w[0]
        V_N = self.v[0]*x[0]
        W_1 = self.W - self.w[0]*x[0]

        self.U = self.calculate_upper_bound(W_1, V_N, i)

        self.m = []
        for i in range(self.n):
            w_min = float('inf')
            for j, w in enumerate(self.w):
                if j > i and w < w_min:
                    w_min = w
            self.m.append(w_min)

        self.z_best = V_N
        self.x_best = x.copy()

        return self.develop(x, i, V_N, W_1)

    def develop(self, x, i, V_N, W_1):
        # print("develop")
        while True:
            if W_1 < self.m[i]:
                if self.z_best < V_N:
                    self.z_best = V_N
                    self.x_best = x.copy()
                    if self.z_best == self.U:
                        return self.finishing()
                return self.backtrack(x, i, V_N, W_1)
            else:
                j_min = min((j for j in range(i+1, self.n) if self.w[j] <= W_1), default = None)
                if (V_N + self.calculate_upper_bound(W_1, V_N, j_min) <= self.z_best) or j_min is None or self.M[i][W_1] >= V_N:
                    return self.backtrack(x, i, V_N, W_1)
                x[j_min] = W_1 // self.w[j_min]
                V_N += self.v[j_min] * x[j_min]
                W_1 -= self.w[j_min] * x[j_min]

                self.M[i][W_1] = V_N
                i = j_min
    
    def backtrack(self, x, i, V_N, W_1):
        # print("back")
        while True:
            j_max = max((j for j in range(i+1) if x[j] > 0), default = None)
            if j_max is None:
                return self.finishing()
            i = j_max
            x[i] -= 1
            V_N -= self.v[i]
            W_1 += self.w[i]
            if W_1 < self.m[i]:
                continue
            if V_N + np.floor(W_1 * (self.v[i+1]/self.w[i+1])) <= self.z_best:
                V_N -= self.v[i] * x[i]
                W_1 += self.w[i] * x[i]
                x[i] = 0
            if W_1 >= self.m[i]:
                return self.develop(x, i, V_N, W_1)
    
    def finishing(self):
        # print("finish")
        result = [0] * (self.n_ori)
        for i, n in enumerate(self.N):
            if n != 0:
                result[n] = self.x_best[1]
        return (self.z_best, result)

    def run(self):
        self.eliminate_dominated_items()
        return self.initialize()

# Example usage
if __name__ == '__main__':
    bnb_knapsack = BnB_knapsack(W=10,
                                v=[10, 7, 5, 2],
                                w=[5, 3, 2, 8])
    best_solution, best_value = bnb_knapsack.run()                 
    print("Best value:", best_value)
    print("Best solution:", best_solution)
