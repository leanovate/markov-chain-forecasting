#!/usr/bin/env python3

from collections import defaultdict, Counter
import numpy as np
from numpy.linalg import inv
from functools import reduce
from statistics import mean
import random

def firstPositiveIndex(l):
    for (index, e) in enumerate(l):
        if e>=0:
            return index

def getNextState(row, currentState):
    r = random.random()
    monteCarlo = reduce(lambda l, e: l + [e+l[-1]] if l else [e], row, [])
    return firstPositiveIndex(np.array(monteCarlo)-r)

def dayUntilDone(tM, startState, numberOfRuns):
    runs = []
    absorbingStates = np.nonzero(tM == 1)[0] # doesn't matter if the take axis 0 or 1 as they both are equal
    for _ in range(numberOfRuns):
        currentState = startState
        daysPassed = 0
        while not currentState in absorbingStates:
            row = tM[currentState]
            currentState = getNextState(row, currentState)
            daysPassed += 1
        runs.append(daysPassed)
    return mean(runs)


def toTransitionMatrix(model, numStates):
    result = np.zeros((numStates, numStates))
    keys = range(numStates)
    absorbingStateCount = 0
    for y in keys:
        sumCount = sum(model[y].values())
        if sumCount == 0:
            result[y][y] = 1 # absorbing transition 
            absorbingStateCount += 1
            continue
        result[y] = [model[y][x]/sumCount for x in keys]
    
    transientStateCount = result.shape[0]-absorbingStateCount
    sMatrix = result[0:transientStateCount,0:transientStateCount]
    qMatrix = inv(np.identity(transientStateCount) - sMatrix)
    
    return (result, qMatrix)

flatten = lambda l: [item for sublist in l for item in sublist]

with open("team1-cycletime.csv") as f:
    dataRows = f.readlines()

dataSet = list(map(lambda row: list(map(int, row.strip("\n").split(","))), dataRows))
NUMBER_OF_STATES = len(set(flatten(dataSet)))

# random.shuffle(dataSet)


split = int(len(dataSet)*0.7)
trainingSet = dataSet[:split]
testingSet = dataSet[split:]

print('Learning model...')
model = defaultdict(Counter)
for row in trainingSet:
    for i in range(len(row) - 1):
        state = row[i]
        nextState = row[i + 1]
        model[state][nextState] += 1

print("MODEL:")
print(model)


(matrix, Q) = toTransitionMatrix(model, NUMBER_OF_STATES)
print(matrix.round(decimals=2))

print()
print("Q&A:")
days = 7
board = [0] * NUMBER_OF_STATES
board[1] = 5
print("How will this board: '{}' look after {} days?".format(board, days))
matrixAfterSomeTime = np.linalg.matrix_power(matrix, days)
borderAfterSomeTime = (board @ matrixAfterSomeTime).round()
print(borderAfterSomeTime)

print()
print("When will a work item in a specific state be done?")
print(np.sum(Q, 1))

print()
monteCarloSimulationCount = 1000
print("MonteCarlo with {} runs:".format(monteCarloSimulationCount))
print("Average days it takes to complete a backlog item: " + str(dayUntilDone(matrix, 0, monteCarloSimulationCount)))

print()
print("Testing:")
startingState = 1 # 0 if all tickets should start in the first column
def getBoardAfterDays(data, numberOfDaysInFuture):
    board = [0] * matrix.shape[0]
    for row in data:
        startingIndex = firstPositiveIndex(np.array(row) - startingState)
        stateAfterDays = row[startingIndex+numberOfDaysInFuture] if startingIndex+numberOfDaysInFuture < len(row) else row[-1]
        board[stateAfterDays]+=1
    return board
testingBoard=getBoardAfterDays(testingSet, 0)
print("How will this board: '{}' look after {} days?".format(testingBoard, days))
def testWherePrediction(numberOfDaysInFuture):
    testResult = getBoardAfterDays(testingSet, numberOfDaysInFuture)
    matrixAfterSomeTime = np.linalg.matrix_power(matrix, numberOfDaysInFuture)
    markovResult = (testingBoard @ matrixAfterSomeTime).round()
    print("Test result: " + str(testResult))
    print("Markov result: " + str(markovResult))
    print("Error: " + str(1/len(testResult)*sum(map(abs, testResult - markovResult))))
    print("Error if we would say nothing changes: " + str(1/len(markovResult)*sum(map(abs, testingBoard - markovResult))))
testWherePrediction(days)


# Questions:
# Where on the board will the item be in 5 days?
# When will this work item be done?
# What will be the final state of the work item?

# Questions that don't work well:
# When will be backlog be emtpy? -> bad, because for the markov chain that indepentent from the size of the backlog


# TODO: add days passed to the states, so that you can ask question about tickets
#       depending how long they have been in a specific state