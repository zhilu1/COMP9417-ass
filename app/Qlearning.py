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
import pickle
import collections
import csv
import copy


class Qlearning:
    def __init__(self, discount_factor, learning_rate, epsilon, action_space, initial_state, useFile):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.action_space = action_space
        self.state = initial_state  # x = x0
        self.useFile = useFile  # load Q table from file or not
        # TODO will it be better to use DataFrame or defaultdict
        self.Q = self.createQTable()
        # self.Q = collections.defaultdict(
        #     lambda: np.zeros(len(self.action_space)))
        self.action = 0
        self.policy = self.createEpsilonGreedyPolicy()

    def createQTable(self):
        if self.useFile:
            return self.loadQtable()
        else:
            return collections.defaultdict(
                lambda: np.zeros(len(self.action_space)))

    def getAction(self):
        # use epsilon greedy policy in execution
        if(self.state.light_delay != 0):
            self.action = 0
            return self.action
        # get probabilities of all actions from current state
        state = str(self.state)
        action_probabilities = self.policy(state)

        # choose action according to
        # the probability distribution
        self.action = np.random.choice(np.arange(
            len(action_probabilities)),
            p=action_probabilities)
        return self.action
        # if(np.random.rand() < self.epsilon):
        #     self.action = np.random.choice(self.action_space)
        # else:
        #     self.action = self.chooseActionByPolicy(self.state)
        # return self.action

    def chooseActionByPolicy(self, state):
        # policy is getting the most rewarding action

        state_str = str(state)
        actions_prop = self.Q[state_str]
        return np.argmax(actions_prop)

    def learn(self, reward, newstate):
        # get newaction using original policy
        newaction = self.chooseActionByPolicy(newstate)

        # update Q table, which is improving the algorithm
        # Q(x,a) = Q(x,a) + learningRate* (reward + discountFactor*Q(newState, newAction) - Q(x,a))
        # print("111111",self.state)
        state_str = str(self.state)
        newstate_str = str(newstate)
        delta = (reward + self.discount_factor *
                 self.Q[newstate_str][newaction] - self.Q[state_str][self.action])
        self.Q[state_str][self.action] += self.learning_rate * delta

        # update state to new state
        self.state = copy.deepcopy(newstate)
        # print("222222", self.state)

    def saveResult(self):
        # print(self.Q)
        keys = self.Q.keys()
        print(len(keys))
        for key in sorted(keys):
            print(key, end='')
            print(self.Q[key])
            np.save('qtable' + 'self.epsilon' + '.npy', np.array(dict(self.Q)))
            # with open('qtable.pkl', 'wb') as file:
            #     pickle.dump(self.Q, file, protocol=pickle.HIGHEST_PROTOCOL)

    def loadQtable(self):
        # load Q table from file if file exists
        try:
            P = np.load('qtable' + 'self.epsilon' + '.npy', allow_pickle=True)
            Q = collections.defaultdict(
                lambda: np.zeros(len(self.action_space)))
            Q.update(P.item())
            return Q
        except (OSError, IOError) as e:
            # if file not exists or error in loading, create an empty defaultdict
            return collections.defaultdict(lambda: np.zeros(len(self.action_space)))

    def createEpsilonGreedyPolicy(self):
        """ 
        Creates an epsilon-greedy policy based 
        on a given Q-function and epsilon. 

        Returns a function that takes the state 
        as an input and returns the probabilities 
        for each action in the form of a numpy array  
        of length of the action space(set of possible actions). 
        """
        def policyFunction(state):
            num_actions = len(self.action_space)
            Action_probabilities = np.ones(num_actions,
                                           dtype=float) * self.epsilon / num_actions

            best_action = np.argmax(self.Q[state])
            Action_probabilities[best_action] += (1.0 - self.epsilon)
            return Action_probabilities

        return policyFunction
