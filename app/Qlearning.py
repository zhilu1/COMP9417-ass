"""
Q learning algorthim

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
    def __init__(self, discount_factor, learning_rate, epsilon, action_space, initial_state, useFile, extra_foldername=''):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.action_space = action_space
        self.state = initial_state  # x = x0
        self.useFile = useFile  # load Q table from file or not
        self.directory = "data0 " + extra_foldername + \
            " discount_factor " + str(self.discount_factor) + \
            " alpha " + str(self.learning_rate) + " epslion " + \
            str(self.epsilon) + " state " + \
            str(self.action_space)  # this is the directory name where we save the results
        self.Q = self.createQTable()
        self.action = 0
        self.policy = self.createEpsilonGreedyPolicy()

    def createQTable(self):
        '''
        create a new empty Q table if self.useFile 
        or load Q table from saved Q table file is file exist 
        '''

        if self.useFile:
            return self.loadQtable()
        else:
            return collections.defaultdict(
                lambda: np.zeros(len(self.action_space)))

    def getAction(self):
        if(self.state.light_delay != 0):
            self.action = 0
            return self.action
        state = str(self.state)
        # get probabilities of all actions from current state
        action_probabilities = self.policy(state)

        # choose action according to
        # the probability distribution
        self.action = np.random.choice(np.arange(
            len(action_probabilities)),
            p=action_probabilities)
        return self.action

    def getBestNextAction(self, state):
        '''
        get the most rewarding result
        '''
        if(state.light_delay != 0):
            # cannot switch
            return 0
        state_str = str(state)
        actions_prop = self.Q[state_str]
        return np.argmax(actions_prop)

    def learn(self, reward, newstate):
        '''
        update Q table based on previous state, action taken and new state and reward generated
        self.state is previous state
        self.action is the action taken
        '''
        # get newaction using original policy
        best_next_action = self.getBestNextAction(newstate)
        state_str = str(self.state)
        newstate_str = str(newstate)
        # update Q table, which is improving the algorithm
        # Q(x,a) = Q(x,a) + learningRate* (reward + discountFactor*Q(newState, newAction) - Q(x,a))

        delta = (reward + self.discount_factor *
                 self.Q[newstate_str][best_next_action] - self.Q[state_str][self.action])
        self.Q[state_str][self.action] += self.learning_rate * delta

        # update state to new state
        self.state = copy.deepcopy(newstate)

    def saveResult(self, x, y):
        '''
        takes in x as the episodes and y as sum of stopped cars at each episode 
        save the Q table to a certain directory
        and save Q table in readable form
        and save save figures
        '''
        keys = self.Q.keys()
        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory)
            except OSError as exc:  # Guard against race condition
                raise
        np.save(os.path.join(self.directory, 'qtable.npy'),
                np.array(dict(self.Q)))
        y_mean = [np.mean(y)]*len(x)
        with open(os.path.join(self.directory, 'qtable.txt'), 'w') as file:
            file.write(str(y_mean))
            for key in sorted(keys):
                file.write(str(key))
                file.write(str(self.Q[key]) + '\n')

        plt.xlabel('Episode')
        plt.ylabel('Stopped Cars Sum')
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
        # plt.show() # show the plot if needed

    def loadQtable(self):
        '''
        load Q table from file if file exists
        '''
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
        ''' 
        Returns a function that takes the state 
        as an input and returns the probabilities 
        for each action in the form of a numpy array  
        of length of the action space(set of possible actions). 
        '''
        def policyFunction(state):
            num_actions = len(self.action_space)
            Action_probabilities = np.ones(num_actions,
                                           dtype=float) * self.epsilon / num_actions

            best_action = np.argmax(self.Q[state])
            Action_probabilities[best_action] += (1.0 - self.epsilon)
            return Action_probabilities

        return policyFunction
