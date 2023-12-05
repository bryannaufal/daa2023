from bnb_knapsack import BnB_knapsack
from dp_knapsack import unboundedKnapsack
import time
import psutil
import os

def evaluasi(capacity, values, weights):

    start = time.time()
    print("running branch and bound")
    branchnbound = BnB_knapsack(capacity, values, weights)
    best_solution, best_value = branchnbound.run()
    mem_usage = psutil.Process().memory_info().rss / 1024 / 1024
    psutil.Process(os.getpid()).memory_info().rss
    end = time.time()
    time_taken = (end-start) * 1000
    print("Branch and Bound Knapsack")
    print("time taken : ", time_taken)
    print("memory usage : ", mem_usage)

    start = time.time()
    print("running dynamic programming")
    best_value, best_solution = unboundedKnapsack(capacity, values, weights)
    mem_usage = psutil.Process().memory_info().rss / 1024 / 1024
    psutil.Process(os.getpid()).memory_info().rss
    end = time.time()
    time_taken = (end-start)*1000
    print("Dynamic Programming Knapsack")
    print("time taken : ", time_taken)
    print("memory usage : ", mem_usage)


if __name__ == '__main__':
    data_list = ["100.txt", "1000.txt", "10000.txt"]
    for data in data_list:
        print("data = ", data)
        with open(data, 'r') as file:
            lines = file.readlines()
            capacity = int(lines[0])
            values = [int(val) for val in lines[1].split(' ')]
            weights = [int(weight) for weight in lines[2].split(' ')]
            evaluasi(capacity, values, weights)
        print("\n \n")
    pass