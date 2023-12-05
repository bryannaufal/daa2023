
# Modified from https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/
def unboundedKnapsack(W, val, wt): 
    n = len(val)
    dp = [0 for i in range(W + 1)] 
    counter = [[0] * n for i in range(W + 1)]

    for i in range(W + 1): 
        for j in range(n): 
            if (wt[j] <= i) and (dp[i] < dp[i - wt[j]] + val[j]): 
                dp[i] = max(dp[i], dp[i - wt[j]] + val[j]) 
                counter[i] = counter[i - wt[j]].copy()
                counter[i][j] += 1

    return dp[W], counter[W]

if __name__ == '__main__':
    W = 100
    val = [10, 30, 20] 
    wt = [5, 10, 15] 

    print(unboundedKnapsack(W, val, wt)) 
