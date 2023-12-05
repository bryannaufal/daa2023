import random

def generate(size):
    values = [random.randint(5, 1000) for _ in range(size)]
    # weights = [random.randint(5, 1000) for _ in range(size)]
    weights = [int(value * random.uniform(0.8, 1.2)) for value in values] # Highly correlated data
    capacity = 10 * size + random.randint(1, size) 
    return capacity, values, weights

def save(filename, capacity, values, weights):
    with open(filename, 'w') as file:
        file.write(f'{capacity}\n')
        file.write(' '.join(map(str, values)) + '\n')
        file.write(' '.join(map(str, weights)) + '\n')

if __name__ == '__main__':
    n = [100, 1000, 10000]
    
    for i in n:
        c,v,w = generate(i)
        save(f'{i}.txt', c,v,w)