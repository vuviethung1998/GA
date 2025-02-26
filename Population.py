import random
import yaml
from Individual import Individual

class Population:
    with open("setting.yaml", 'r') as stream:
        config =yaml.load(stream ,Loader= yaml.FullLoader)
    pc1p = config['pc1p']
    pc2p = config['pc2p']
    pBLX = config['pBLX']
    pAMOX = config['pAMOX']
    sm =config['sigma']
    def __init__(self, size, sigma, f):
        self.sigma = sigma
        self.size = size
        self.pop = []
        self.fitness = f
        for i in range(self.size):
            ind = Individual(sigma)
            ind.value_fitness = self.fitness(ind)
            self.pop.append(ind)
        
    
    def  crossover_one_point(self, parent1, parent2):
        n1 = random.randint(1,len(parent1)-1)
        child1 = [0]*len(parent1)
        child2 = [0]*len(parent1)
        for i in range(0, n1):
            child1[i] = parent1[i]
            child2[i] = parent2[i]
        for i in range(n1, len(parent1)):
            child1[i] = parent2[i]
            child2[i] = parent1[i]
        return [child1, child2]
    
    
    def crossover_two_point(self, parent1, parent2):
        n1 = random.randint(0,len(parent1) -1)
        n2 = random.randint(0,len(parent1) -1)
        while n1 == n2:
            n2 = random.randint(0,len(parent1) -1)

        if n1 > n2:
            n1, n2 = n2, n1
        child1 = [0]*len(parent1)
        child2 = [0]*len(parent1)
        for i in range(0, n1):
            child1[i] = parent1[i]
            child2[i] = parent2[i]
        for i in range(n1, n2+1):
            child1[i] = parent2[i]
            child2[i] = parent1[i]
        for i in range(n2+1, len(parent1)):
            child1[i] = parent1[i]
            child2[i] = parent2[i]
        return [child1, child2]

    def BLX(self, parent1, parent2):
        n1 = parent1
        n2 = parent2
        if n1 > n2:
            n1, n2 = n2, n1
        alpha = int((n2 - n1)/2)
        n2 += alpha
        n1 -= alpha
        if n1 < 2 :
            n1 = 2
        return random.randint(n1, n2)

    def AMOX(self, parent1, parent2):
        alpha = random.random()
        return int( alpha*parent1 + (1- alpha)*parent2 ) 
    

    def crossover(self, parent1, parent2):
        child1 = Individual(self.sigma)
        child2 = Individual(self.sigma) 
        r = random.random()
        if r < Population.pc1p:
            a = self.crossover_one_point(parent1.genes, parent2.genes)
            child1.set_genes(a[0])
            child2.set_genes(a[1])
        else:
            a = self.crossover_two_point(parent1.genes, parent2.genes)
            child1.set_genes(a[0])
            child2.set_genes(a[1])
        
        if r < Population.pAMOX:
            child1.set_n(self.AMOX(parent1.n, parent2.n))
            child2.set_n(self.AMOX(parent1.n, parent2.n))
        else:
            child1.set_n(self.BLX(parent1.n, parent2.n))
            child2.set_n(self.BLX(parent1.n, parent2.n))
        
        child1.value_fitness = self.fitness(child1)
        child2.value_fitness = self.fitness(child2)
        return [child1, child2]

    def mutation(self, ind):
        parent1 = ind.genes
        child1 = [ i for i in parent1]
        s = 0
        for i in range(len(parent1)):
            s += (1-self.sigma[i], self.sigma[i])[parent1[i] == 0] 
        k = random.random()*s
        a =0
        for i in range(len(parent1)):
            if a <= k <= a + (1-self.sigma[i], self.sigma[i])[parent1[i] == 0]:
                child1[i] = 1 - child1[i]
                break
        child = Individual(self.sigma)
        child.set_genes(child1)
        child.set_n(int(random.gauss(ind.n, Population.sm)))
        child.value_fitness = self.fitness(child)
        return [child]
    
    
    def get_best(self):
        max_value_fitness = 0
        for i in range(self.size):
            if max_value_fitness < self.pop[i].value_fitness:
                max_value_fitness = self.pop[i].value_fitness
        for i in range(self.size):
            if self.pop[i].value_fitness == max_value_fitness:
                return self.pop[i]
    
    def selection(self):
        self.pop = sorted(self.pop, key= lambda x : -x.value_fitness)
        self.pop = self.pop[0:self.size]