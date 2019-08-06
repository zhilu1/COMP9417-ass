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
import json
import os
import matplotlib.pyplot as plt


class Qlearning:
    def __init__(self, discount_factor, learning_rate, epsilon, action_space, initial_state, useFile):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.action_space = action_space
        self.state = initial_state  # x = x0
        self.useFile = useFile  # load Q table from file or not
        # TODO will it be better to use DataFrame or defaultdict
        self.directory = "data0 " + \
            " discount_factor " + str(self.discount_factor) + \
            " alpha " + str(self.learning_rate) + " epslion " + \
            str(self.epsilon) + " state " + str(self.action_space)
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

    def getBestNextAction(self, state):
        # policy is getting the most rewarding action
        if(state.light_delay != 0):
            # cannot switch
            return 0
        state_str = str(state)
        actions_prop = self.Q[state_str]
        return np.argmax(actions_prop)

    def learn(self, reward, newstate):
        # get newaction using original policy
        best_next_action = self.getBestNextAction(newstate)
        state_str = str(self.state)
        newstate_str = str(newstate)
        # if(newstate.light_delay != 0):
        #     self.Q[newstate_str][1] = -999
        # if(self.state.light_delay != 0):
        #     self.Q[state_str][1] = -999

        # update Q table, which is improving the algorithm
        # Q(x,a) = Q(x,a) + learningRate* (reward + discountFactor*Q(newState, newAction) - Q(x,a))
        # print("111111",self.state)

        delta = (reward + self.discount_factor *
                 self.Q[newstate_str][best_next_action] - self.Q[state_str][self.action])
        self.Q[state_str][self.action] += self.learning_rate * delta

        # update state to new state
        self.state = copy.deepcopy(newstate)
        # print("222222", self.state)

    def saveResult(self, x, y):
        # print(self.Q)
        keys = self.Q.keys()
        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory)
            except OSError as exc:  # Guard against race condition
                raise
        np.save(os.path.join(self.directory, 'qtable.npy'),
                np.array(dict(self.Q)))
        # print(len(keys))
        y_mean = [np.mean(y)]*len(x)
        with open(os.path.join(self.directory, 'qtable.txt'), 'w') as file:
            file.write(str(y_mean))
            for key in sorted(keys):
                file.write(str(key))
                file.write(str(self.Q[key]) + '\n')

                # file.write(json.dumps(self.Q))
        plt.xlabel('Episode')
        plt.ylabel('Reward Sum')
        fig, ax = plt.subplots()
        dataline = ax.plot(
            x, y, label='Data', marker=',')
        mean_line = ax.plot(x, y_mean,
                            label='Mean', linestyle='--')

        # Make a legend
        legend = ax.legend(loc='upper right')
        if self.useFile:
            plt.savefig(os.path.join(self.directory,
                                     'plot testing' + type(self).__name__))
            plt.title(self.directory + ' plot testing' + type(self).__name__)
        else:
            plt.savefig(os.path.join(self.directory,
                                     'plot training' + type(self).__name__))
            plt.title(self.directory + ' plot training' + type(self).__name__)
        plt.close(fig)
        # plt.show()

    def loadQtable(self):
        # load Q table from file if file exists
        try:
            P = np.load(os.path.join(self.directory,
                                     'qtable.npy'), allow_pickle=True)
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
