'''
Fixed switch strategy
All lights will be switched together per 10 time-step
'''

import matplotlib.pyplot as plt
import numpy as np


class FixedSwitch:
    def __init__(self):
        self.steps = 1

    def getAction(self):
        if self.steps >= 10:
            self.steps = 1
            return 1  # switch both
        else:
            self.steps += 1
            return 0  # switch neither

    def learn(self, reward, newstate):
        # Fixed policy doesn't learn
        pass

    def saveResult(self, x, y):
        plt.xlabel('Episode')
        plt.ylabel('Stopped Cars Sum')
        fig, ax = plt.subplots()
        dataline = ax.plot(
            x, y, label='Data', marker=',')
        y_mean = [np.mean(y)]*len(x)
        mean_line = ax.plot(x, y_mean,
                            label='Mean', linestyle='--')

        # Make a legend
        legend = ax.legend(loc='upper right')
        plt.savefig("Fixed switch")
