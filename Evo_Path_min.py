#parsa badiei

import random


path = './'
positions = []

def start():
    global positions
    positions =  get_positions(path+"Positions_(cities).txt")
    p= int (input('population ? '))
    u= int (input('number of parents ? '))
    l = p-u
    preparefile()
    fitness=[20000]
    iteration = 0
    population= createPopulation(p, positions)

    while not IsFinished( iteration , fitness):
        
        fitness = EvaluatePopulation(population)
        parents = poolOfParents(u , population , fitness)
        stats(EvaluatePopulation(parents),iteration)
        newGeneration = inheritance(parents , l)
        population = newGeneration.copy()
        iteration +=1
    finishUp(population , fitness)
    return

def preparefile():
    file = open(path + "results-min.txt", 'w')
    file.write("minimization\n#\t\tMax\t\tMean\t\tmin\n\n")
    file.close()

def get_positions(filename):
    global positions
    file = open(filename).readlines()
    del file[0]
    positions = []
    for line in file:
        arrayline = line.split('\t')[1:-1]
        arrayline[0] = int(arrayline[0])
        arrayline[1] = int(arrayline[1])
        positions.append(arrayline)
    print('number of cities:',len(positions))

    return positions

def createGnome(positions):
    gnome=[]
    copyofcities = positions*2
    while copyofcities.__len__()>0:
        r = random.randint(0,copyofcities.__len__()-1)
        if not gnome.__len__()==0 and not copyofcities.__len__()==1 and gnome[-1][0] == copyofcities[r][0] and gnome[-1][1] == copyofcities[r][1]:
            continue
        gnome.append(copyofcities[r])
        del copyofcities[r]
        #print('lencities',copyofcities.__len__(),end=' ')

    #correct for illegal gnomes
    if(gnome[-1][0] == gnome[-2][0] and gnome[-1][1] == gnome[-2][1]):
        temp = gnome[0]
        gnome[0] = gnome[-2]
        gnome[-2] = temp

    return gnome

def createPopulation(p, positions):
    population = []
    for x in range(p):
        population.append(createGnome(positions))
    return population

def fitnessEvaluation(gnome):
    fitness = 0
    for x in range(len(gnome)-1):
        fitness += abs(gnome[x][0] - gnome[x+1][0]) + abs(gnome[x][1] - gnome[x+1][1])
    return fitness

def EvaluatePopulation(population):
    fitness = []
    for i in population:
        fitness.append(fitnessEvaluation(i))
    return fitness

def IsFinished(iteration , fitness):
    if min(fitness) < 2000 or iteration>1000:
        return True
    else:
        return False

def poolOfParents(u , pop, fit):
    parents=[]
    population = pop.copy()
    fitness = fit.copy()
    #rank based parent selection
    for x in range(u):
        i = fitness.index(min(fitness))
        parents.append(population[i])
        del fitness[i]
        del population[i]
    return parents


def inheritance(pool,landa):
    newGeneration = pool.copy()
    p1=[]
    p2=[]
    for i in range(landa):
        p1 =pool[random.randint(0,len(pool)-1)]
        p2 =pool[random.randint(0, len(pool) - 1)]
        c1 = []
        crosspoint = random.randint(0,len(p1)-1)
        c1 += p1[0:crosspoint]
        c1 += p2[crosspoint:]
        newGeneration.append(c1)
    
    return newGeneration


def checkadjacentcities(newGen):
    for indi in newGen:
        for x in range(indi.__len__()-1):
            if indi[x][0] == indi[x+1][0] and indi[x][1] == indi[x+1][1] :
                indi = createGnome(positions)

    return newGen
def mutation(pop):
    #flipping two cities
    m = int(0.1*len(pop))
    r11 = random.randint(0,len(pop)-1)
    r12 = random.randint(0,len(pop[0])-1)
    r21 = random.randint(0,len(pop)-1)
    r22 = random.randint(0,len(pop[0])-1)
    for i in range(m):
        temp = pop[r11][r12]
        pop[r11][r12] = pop [r21][r22]
        pop[r21][r22] = temp

def stats(fitness,iter):
    Max = max(fitness)
    m = min(fitness)
    mean = round(sum(fitness) / len(fitness),1)

    file = open(path+"results-min.txt",'a')
    strToWrite = str(iter)+'\t\t'+str(Max)+'\t\t'+str(mean)+'\t\t'+str(m)+'\n'
    file.write(strToWrite)

def finishUp(pop , fit):
    file = open(path+"FinalPath-min.txt", 'w')
    bestIndividual = pop[fit.index(max(fit))]
    coordinates = ''
    for cord in bestIndividual:
        coordinates += str(cord[0])+'\t\t'+str(cord[1])+'\n'
    maxfitness = 'min fitness: '+ str(min(fit)) +'\n\n'
    strtowrite = maxfitness + coordinates
    file.write(strtowrite)
    print(strtowrite)


start()


def test():
    p = [1,2,3,4,2,1,4]
    p[4:] = [7,7,7]
    print(p)
    return


