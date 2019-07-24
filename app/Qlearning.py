"""
State = 
closest car position from intersection for road 1 (0-8, 9 if no cars) X
closest car position from intersection for road 2 (0-8, 9 if no cars X
light setting (ie 0-green, 1 red for one of the roads) X
light delay (0-3)

Two actions: decide to switch or not.

Reward -1.0 if a car is stopped at a red light on either road, zero
otherwise.

Optimise discounted sum of future reward.

Use discount factor: gamma = .9

Use learning rate: alpha = .1

Epsilon-greedy exploration 10%

Plot and compare performance measures for both the fixed switching and
learnt policies. 


"""
import numpy as np

import collections
import csv


class Qlearning:
    def __init__(self, discount_factor, learning_rate, epsilon, action_space, initial_state):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.action_space = action_space
        # Q(x,a) = 0 for all x,a
        Q = collections.defaultdict(lambda: np.zeros(len(action_space)))
        self.state = initial_state  # x = x0
        # policy is a dictionary that takes a state and return a list indexed by action containing action prob

    def getAction(self):
        # use epsilon greedy policy in execution
        if(np.random.rand() < self.epsilon):
            return np.random.choice(self.action_space)
        else:
            return self.chooseActionByPolicy(self.state)

    def chooseActionByPolicy(self, state):
        # policy is getting the most rewarding action
        return np.argmax(self.Q[state])

    def learn(self, reward, newstate):
        # get newaction using original policy
        newaction = self.chooseActionByPolicy(newstate)
        # update Q table, which is improving the algorithm
        # Q(x,a) = Q(x,a) + learningRate* (reward + discountFactor*Q(newState, newAction) - Q(x,a))
        self.Q[state][action] += self.learning_rate * \
            (reward + self.discount_factor *
             self.Q[newstate][newaction] - self.Q[self.state][self.action])
        # update state to new state
        self.state = newstate

    def saveResult(self):
        with open('Qlearning_table.csv', 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile)
            csvwriter.writerows(self.Q)
