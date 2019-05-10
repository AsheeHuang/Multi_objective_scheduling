from Dispatch_Rule import Machine_Oriented
from ReadData import *
import random
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from DEA import DEA_analysis
import numpy as np



def weights_generater(n = 6) :
    weights = [-1 for _ in range(n)]
    for i in range(n) :
        weights[i] = random.random() if random.random() > 0.35 else  0
    sum_ = sum(weights)
    if sum_ == 0 :
        return [1/n for _ in range(n)]

    for i in range(n) :
        weights[i] /= sum_
    return weights
def weights_generater2(n = 6) :
    weight = [0 for i in range(n)]
    weight[random.randint(0,5)] = 1
    return weight
class NSGA(object) :
    class Gene(object) :
        def __init__(self,nsga,weights):
            self.nsga = nsga
            self.weights = weights
            late,ft,pieces,_ = Machine_Oriented(nsga.J,nsga.common_due_date,weights)

            self.obj = [late,ft,pieces]

            self.dist = None
        def dominate(self,gene2):
            if self.obj[0] <= gene2.obj[0] and self.obj[1] <= gene2.obj[1] and self.obj[2] >= gene2.obj[2] :
                return True
            return False

        def point_mutation(self):
            k = random.randint(0, 5)
            # print(r,i,len(self.pop))
            if self.weights[k] > 0:
                self.weights[k] = 0
            else:
                self.weights[k] = random.random()
            sum_ = sum(self.weights)
            if sum_ == 0:
                self.weights[k] = 1
                sum_ = sum(self.weights)
            for i in range(6):
                self.weights[i] /= sum_
            late, ft, pieces, _ = Machine_Oriented(self.nsga.J, self.nsga.common_due_date, self.weights)
            self.obj = [late, ft, pieces]

        def swap_mutation(self):
            idx1, idx2 = random.sample([i for i in range(0, 6)], 2)
            self.weights[idx1], self.weights[idx2] = self.weights[idx2], self.weights[idx1]
            late, ft, pieces, _ = Machine_Oriented(self.nsga.J, self.nsga.common_due_date, self.weights)
            self.obj = [late, ft, pieces]
    def __init__(self,population,generation,crossover_rate = 0.8, mutation_rate = 0.3, Job_set = None, common_due_date = 60):
        self.population = population
        self.generation = generation
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.pop = []
        self.common_due_date = common_due_date
        self.J = Job_set
        for _ in range(self.population) :
            self.pop.append(self.Gene(self,weights_generater()))

    def run(self):

        for gen in range(self.generation) :
            print(gen)
            parents = []
            Front_L = []
            for _ in range(self.population) :
                fid,mid = random.sample([i for i in range(self.population)],2)
                self.pop += [self.normal_crossover(self.pop[fid],self.pop[mid])]
            F = self.nondominated_sort()
            for i in range(len(F)) :
                if len(parents) + len(F[i]) > self.population :
                    self.Crowding_Dist(F[i])
                    Front_L  = F[i]
                    break
                else :
                    parents += F[i]

            if len(parents) < self.population :
                k = self.population - len(parents)
                # print(Front_L,parents)
                Front_L.sort(key = lambda x : x.dist,reverse=True)
                parents += (Front_L[:k])

            self.pop = parents
            # self.mutation(self.population // 10)
            # self.plot()

    def mutation(self, target, strategy = 0) :
        if strategy == 0 :
            if random.random() < 0.5 :
                target.swap_mutation()
            else :
                target.point_mutation()
        elif strategy == 1 :
            target.point_mutation()
        else :
            target.swap_mutation()


    def nondominated_sort(self,remain = False):
        Sp = set()
        F = [[]]
        n = [0 for _ in range(len(self.pop))]
        for p in range(len(self.pop)) :
            for q in range(len(self.pop)) :
                if p != q :
                    if self.pop[p].dominate(self.pop[q]) :
                        Sp.add(self.pop[q])
                    elif self.pop[q].dominate(self.pop[p]) :
                        n[p] += 1
            if n[p] == 0 :
                F[0].append(self.pop[p]) #first front
        i = 0

        while F[i]:
            H = []
            for p in range(len(F[i])) :
                for q in range(len(Sp)) :
                    n[q] -= 1
                    if n[q] == 0 :
                        H.append(self.pop[q])
            i = i + 1
            F.append([])
            F[i] = H
        if remain == True :
            for i in range(len(self.pop)) :
                if n[i] > 0 :
                    F[-1].append(self.pop[i])
        return F
    def Crowding_Dist(self,F):
        N = len(F)

        for i in range(N) :
            F[i].dist = 0

        for m in range(3) :
            F.sort(key = lambda x : x.obj[m])
            F[0].dist,F[N-1].dist = float('inf'),float('inf')
            for i in range(1,N-1) :
                F[i].dist += (F[i+1].obj[m] - F[i-1].obj[m]) / ((F[N-1].obj[m] - F[0].obj[m]) +1 )
        # for i in range(N) :
        #     print(F[i].dist)

    def linear_crossover(self,c1,c2):
        child1_weight = []
        child2_weight = []

        for i in range(len(c1.weights)) :
            rand = random.random()
            child1_weight.append(c1.weights[i] * rand + c2.weights[i] * (1 - rand))
            child2_weight.append(c2.weights[i] * rand + c1.weights[i] * (1 - rand))
        child1 = self.Gene(self, child1_weight)
        child2 = self.Gene(self, child2_weight)

        if random.random() <= 0.1 :
            self.mutation(child1)
        elif random.random() <= 0.1 :
            self.mutation(child2)
        return [child1, child2]

    def normal_crossover(self,c1,c2) :
        child_weight = []
        for i in range(len(c1.weights)) :
            child_weight.append((c1.weights[i] + c2.weights[i]) / 2)
        child = self.Gene(self,child_weight)
        return child


    def plot(self,alpha = 1):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        F = self.nondominated_sort(remain = False)
        for i in range(len(F)) :
            c = None
            if i == 0:
                c = 'r'
            elif i == 1:
                c = 'b'
            else :
                c = "g"
            for j in F[i] :
                if c == 'r' :
                    ax.scatter(j.obj[0],j.obj[1],j.obj[2],c = c,alpha = 1)
                else :
                    ax.scatter(j.obj[0], j.obj[1], j.obj[2], c=c, alpha = alpha)
        ax.set_xlabel("Tardiness")
        ax.set_ylabel("Flow Time")
        ax.set_zlabel("Pieces")
        plt.show()





if __name__ == "__main__" :
    path = './Experiment_Data1/data_1_200'
    J = []
    ReadData(path, J)
    ga = NSGA(3000,5,Job_set=J,common_due_date = 120)
    ga.run()
    pareto = ga.nondominated_sort()[0]

    input = [[] for _ in range(2)]
    output = [[]]

    for point in pareto :
        input[0].append(point.obj[0])
        input[1].append(point.obj[1])
        output[0].append(point.obj[2])
    ga.plot(0.5)
    res = (DEA_analysis(input, output))
    for idx,r in enumerate(res):
        print("SPT : %.2f, HVF : %.2f, LP : %.2f, EDD : %.2f, FIFO : %.2f, SST : %.2f, DEA Efficiency : %.2f"
              %(pareto[idx].weights[0],pareto[idx].weights[1],pareto[idx].weights[2],pareto[idx].weights[3],pareto[idx].weights[4],pareto[idx].weights[5],r["Efficiency"]))
