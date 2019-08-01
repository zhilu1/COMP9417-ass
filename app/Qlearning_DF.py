import numpy as np
import pandas as pd
#import os.path


class Qlearning:
	def __init__(self, discount_factor, learning_rate, epsilon, action_space, initial_state, useFile):
		self.discount_factor = discount_factor # discount factor = 0.9
		self.learning_rate = learning_rate # learning rate = 0.1
		self.epsilon = epsilon # epsilon greedy = 0.1
		self.action_space = action_space # switch/not switch (action_space=[0, 1])
		self.state = initial_state  # x = x0
		self.useFile = useFile  # load Q table from file or not
		self.q_table = self.createQTable()
#		self.action = 0	
		
	def createQTable(self):
		if self.useFile:
			return pd.read_csv('qtable.txt')
		else:
			return pd.DataFrame(columns=self.action_space, dtype=np.float64)
			
	def getAction(self,state):
		if(state.light_delay != 0):
			action = 0
			return action
		
		state = str(state)
		if state not in self.q_table.index:
			new_state = pd.Series([0]*len(self.action_space), index=self.q_table.columns, name=state)
			self.q_table = self.q_table.append(new_state)
		# use epsilon greedy policy in execution
		if(np.random.rand() < self.epsilon):
			action = np.random.choice(self.action_space)
		else:
			action = self.chooseActionByPolicy(state)
		return action
	
	def chooseActionByPolicy(self, state):
		# policy is getting the most rewarding action	
		state_reward = self.q_table.loc[state, :]
		if state_reward.max() == state_reward.min(): # same reward: choose randomly
			action = np.random.choice(self.action_space)
		else:
			action = state_reward.idxmax()
		return action	
		
	def learn(self,action, reward, state, newstate):
		# append a new state to q-table
		if newstate not in self.q_table.index:
			new_state = pd.Series([0]*len(self.action_space), index=self.q_table.columns, name=newstate)
			self.q_table= self.q_table.append(new_state)
			
		# get newaction using original policy	
#		newaction = self.chooseActionByPolicy(newstate)

		# update Q table, which is improving the algorithm
		# Q(x,a) = Q(x,a) + learningRate* (reward + discountFactor*Q(newState, newAction) - Q(x,a))

		self.q_table.loc[state, action] += self.learning_rate * (reward + self.discount_factor * self.q_table.loc[newstate, :].max() - self.q_table.loc[state, action])

	def saveQtable(self):
		self.q_table.to_csv('qtable.txt')
	
	
#	def saveResult(self):
##		print(self.Q)
#		if self.useFile == False:
#			with open('qtable.txt', 'w') as f:
#				for row 
#				f.write(str(self.q_table))
#			f.close()
			
		
		
		
		
	
			
	
	
	