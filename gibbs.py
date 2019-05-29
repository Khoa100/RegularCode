# -*- coding: utf-8 -*-
"""

@author: Minhkhoa Vu, 014007797
"""
import sys
import random as r
import math
from functools import reduce
""" To understand how the reduce function works, I went to this link:
https://www.geeksforgeeks.org/reduce-in-python/ """

""" A Bayesian Network is not necessary because we already have information
about each of the nodes. For example, we know that the markov blanket of 'cloudy' is 
'sprinkler' and 'rain'. The parents of the node 'rain' is cloudy.
Wetgrass has  
In addition, this Bayesian network has been illustrated and
discussed in lecture. As a result, no object-oriented programming is necessary for this
project."""

parentData = {
    'cloudy': [],
    'sprinkler': ['cloudy'],
    'rain': ['cloudy'],
    'wetgrass': ['sprinkler', 'rain']
}
childrenData = {
    'cloudy': ['sprinkler', 'rain'],
    'sprinkler': ['wetgrass'],
    'rain': ['wetgrass'],
    'wetgrass': []
}

"""these 4 functions return values based on what is provided; 
cloudyConstant() is an exception"""
def cloudyConstant():
    return 0.5

def getSprinklerVal(cloudy):
    return 0.1 if cloudy else 0.5

def getRainVal(cloudy):
    return 0.8 if cloudy else 0.2

def getWetgrassVal(sprinkler, rain):
    if sprinkler and rain:
        return 0.99
    elif sprinkler and not rain:
        return 0.90
    elif not sprinkler and rain:
        return 0.90
    else:  # s and !r or !s and r
        return 0.00

#convert parent list to a dictionary and return it
def convertVarListToMap(variables, state):
    varDictionary = {} #new dictionary to be returned
    for curVar in variables:
        varDictionary[curVar] = state[curVar]
    return varDictionary

#calculate the parent probability of a queried variable
"""This portion is needed because the values obtained from getSprinklerVal()
or getWetgrassVal() is not static. Although we are given both of them to be true statements,
the provided probabilities are not the same, since 4 different scenarios can happen when given
sprinkler to be true and wetgrass to be true"""
def calculateParentProb(varQueried, state):
    # get the raw list of parents
    nodeparent = parentData[varQueried]

    # convert list into dict given state
    #no need to do this if nodeparent is empty (varQueried == cloudy)
    nodeparent = convertVarListToMap(nodeparent, state)  # {'c': 0}
    prob = 0
    if varQueried == 'cloudy':
        prob = cloudyConstant()
    elif varQueried == 'rain':
        rainVal = getRainVal(nodeparent['cloudy'])
        if state[varQueried] == 0:
            prob = 1-rainVal
        else:
            prob = rainVal
    elif varQueried == 'sprinkler':
        sprinkVal = getSprinklerVal(nodeparent['cloudy'])
        if state[varQueried] == 0:
            prob = 1-sprinkVal
        else:
            prob = sprinkVal
    elif varQueried == 'wetgrass':
        wetVal = getWetgrassVal(sprinkler=nodeparent['sprinkler'], rain=nodeparent['rain'])
        if state[varQueried] == 0:
            prob = 1-wetVal
        else:
            prob = wetVal
    else:
        # something went wrong; look into
        prob = -math.inf

    return prob

# compute conditional probability of a queried variable
def calculateConditionalProb(queryVar, state):

    # loop through true and false values
    true_falseArr = []
    tfArr = [1, 0]

    # important loop - R can be true or false
    for _tf in tfArr:
        state[queryVar] = _tf

        # P(x | par(x))
        parentProb = calculateParentProb(queryVar, state)

        # [P(y | par(y) for y in child(x))
        childlist = [calculateParentProb(y, state) for y in childrenData[queryVar]]
        #I went to the following website to understand the lambda function: https://stackoverflow.com/questions/6076270/python-lambda-function-in-list-comprehensions"
        b = reduce(lambda val1, val2: val1*val2, childlist)

        p = parentProb * b #P((!)r|(!)c) or P(c|s,r)
        true_falseArr.append(p)

    p = normalize(true_falseArr)
    return p[0]  # the true value

variables = ['cloudy','rain','sprinkler','wetgrass']
#gibbs sampling implementation, based on algorithm provided in the book
def gibbsSampling(queryVariable,numTrials, evidenceVariables):
    N = {1: 0, 0: 0}
    Z = [x for x in variables if x not in evidenceVariables]  # ['c', 'r'] -> non-evidence vars
    state = evidenceVariables
    for z in Z:  # randomly init the non-evidence vars
        state[z] = r.randint(0, 1)

    for j in range(int(numTrials)):
        for zVal in Z:
            probZ = calculateConditionalProb(zVal, state)
            zInitial = int(r.uniform(0.0, 1.0) < probZ)
            state[zVal] = zInitial
            N[state[queryVariable]] += 1

    return normalize(list(N.values()))

def normalize(arr):
    #round the probability vector to 4 decimal places
    return [round(float(k)/sum(arr),4) for k in arr]

# answer to P(R | s, w)
if __name__ == "__main__":
    evidence_variables = {'sprinkler': 1, 'wetgrass': 1}
    #probabilityVector = gibbsSampling(sys.argv(1), evidence_variables.copy())
    probabilityVector = gibbsSampling(variables[1],10000, evidence_variables.copy())
    print('<{0}, {1}>'.format(probabilityVector[0], probabilityVector[1]))

    
    
            
    
        

    
        
    
