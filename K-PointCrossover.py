# The idea of this programme is to solve a mixed integer programming optimization problem using GA Algorithm.

# With this programme, even if it's a totally different question, the user only needs to change the parameters under the
# section GA parameters. There is no need to change anything in the other parts of the code. This makes the programme
# more user-friendly for people who do not have background in coding and is more susceptible for future use.


import random                                   # the random library is used for pseudo-random number generation


# GA parameters
lengthOfChromosome = 7                          # binary code has 7 digits
population = []
populationValue = []
Pj = []
parents = []
cuttingPoint = []
solution = []
Pm = 0.02                                       # probability of mutation
populationSize = 100
iterations = 200
valueData = (30, 60, 25, 8, 10, 40, 60)         # the value of each item
weightData = (40, 40, 30, 5, 15, 35, 30)        # the weight of each item


# Generate the first generation of the population by pseudo-random number generation
def generateFirstGen():
    for i in range(populationSize):
        temp = ''
        for j in range(lengthOfChromosome):
            temp2 = random.randint(0, 1)
            if temp2 == 0:
                temp += '0'
            else:
                temp += '1'
        population.append(temp)


# Kill all population whose weight is over 120KG
def killOverweight():
    temp = []
    for i in range(populationSize):
        weight = 0
        for j in range(lengthOfChromosome):
            weight += int(population[i][j]) * weightData[j]
        if weight <= 120:
            temp.append(population[i])
    population.clear()
    for i in range(len(temp)):
        population.append(temp[i])


# Generate a list of the values represented by each population member
def populationValueGeneration():
    populationValue.clear()
    for i in range(len(population)):
        value = 0
        for j in range(lengthOfChromosome):
            value += int(population[i][j]) * valueData[j]
        populationValue.append(value)


# Generate the Pj of each population member
def PjGeneration():
    Pj.clear()
    for i in range(len(populationValue)):
        Pj.append(populationValue[i] / sum(populationValue))


# Generate a list of parents for the reproduction of the next generation
def chooseParents():
    parents.clear()
    for i in range(int(populationSize / 2)):
        temp = random.randint(0, 100) / 100
        cumulative = 0
        index = -1
        for j in range(len(Pj)):
            if cumulative < temp:
                cumulative += Pj[j]
                index += 1
        p1 = population[index]
        temp2 = random.randint(0, 100) / 100
        cumulative2 = 0
        index2 = -1
        for k in range(len(Pj)):
            if cumulative2 < temp2:
                cumulative2 += Pj[k]
                index2 += 1
        p2 = population[index2]
        parents.append([p1, p2])


# Generate a list of cutting point for the reproduction of the next generation
# K-Point Crossover is used
def cuttingPointGeneration():
    cuttingPoint.clear()
    for i in range(int(populationSize / 2)):
        cuttingPoint.append([])
        k = random.randint(0, 6)
        while len(cuttingPoint[i]) < k:
            cut = random.randint(1, 6)
            if cut not in cuttingPoint[i]:
                cuttingPoint[i].append(cut)
        cuttingPoint[i].sort()


# Generate the next generation
# K-Point Crossover is used
def produceOffspring():
    population.clear()
    for i in range(len(parents)):
        offSpring1 = ''
        offSpring2 = ''
        for j in range(7):
            if j in cuttingPoint[i]:
                offSpring1, offSpring2 = offSpring2, offSpring1
            offSpring1 += parents[i][0][j]
            offSpring2 += parents[i][1][j]
        population.append(offSpring1)
        population.append(offSpring2)


# Mutate the population
def populationMutate():
    for i in range(len(population)):
        for j in range(lengthOfChromosome):
            temp = random.randint(0, 100) / 100
            if temp <= Pm:
                store = ''
                for k in range(j):
                    store += population[i][k]
                if population[i][j] == '0':
                    store += '1'
                else:
                    store += '0'
                for k in range(lengthOfChromosome - 1 - j):
                    store += population[i][k - lengthOfChromosome + 1]
                population[i] = store


# def decimalToBinary(decimal):
#     binary = ''
#     while decimal != 0:
#         if decimal % 2 == 1:
#             binary = '1' + binary
#         else:
#             binary = '0' + binary
#         decimal = decimal // 2
#     if len(binary) != lengthOfChromosome:
#         for i in range(lengthOfChromosome - len(binary)):
#             binary = '0' + binary
#     return binary
#
#
# def binaryToDecimal(binary):
#     decimal = 0
#     for i in range(len(binary)):
#         decimal += (2 ** i) * int(binary[- i - 1])
#     return decimal


def main():
    generateFirstGen()
    killOverweight()
    populationValueGeneration()
    for i in range(iterations + 1):
        PjGeneration()
        chooseParents()
        cuttingPointGeneration()
        produceOffspring()
        populationMutate()
        killOverweight()
        populationValueGeneration()
        # Outputting the results of each iteration
        if i == 1:
            print('\nThe maximum result of each generation is shown below:\n')
        if i != 0:
            if i % 5 != 0 and i != iterations:
                print('Generation' + ' ' * (len(str(iterations)) + 1 - len(str(i))) + str(i) + ': ' + str(populationValue[populationValue.index(max(populationValue))]), end = '     ')
            else:
                print('Generation' + ' ' * (len(str(iterations)) + 1 - len(str(i))) + str(i) + ': ' + str(populationValue[populationValue.index(max(populationValue))]))
            if i == iterations:
                weight = 0
                for j in range(lengthOfChromosome):
                    weight += int(population[populationValue.index(max(populationValue))][j]) * weightData[j]
                for j in range(lengthOfChromosome):
                    if population[populationValue.index(max(populationValue))][j] == '1':
                        solution.append(str(j + 1))
                print('\nThe final result is shown below:')
                print('The optimal binary code is ' + population[populationValue.index(max(populationValue))] + '.')
                print('This means that the optimal solution is to put items ', end = '')
                for j in range(len(solution) - 1):
                    print(solution[j] + ', ', end = '')
                print('and ' + solution[-1] + ' into the container.')
                print('The total value of the items is ' + str(populationValue[populationValue.index(max(populationValue))]) + ' and the total weight is ' + str(weight) + 'KG.')


main()
