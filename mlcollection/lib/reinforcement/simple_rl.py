'''
Created on Mar 23, 2010
@author: Zachary Varberg
'''

from numpy import *
import scipy as Sci
import scipy.linalg
import copy
from matplotlib import pyplot 

import abstract_rl
import lib.matplotlib_util as mpl_util

class Simple_RL(abstract_rl.AbstractReinforcementLearner):
    
    def __init__(self, alpha, gamma, num_states=(15,15)):
        self.num_states = num_states[0]*num_states[1]
        self.dimensions = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.curr_state = self.get_start_state()
        self.num_actions = 4
        self.Q_mat = zeros((self.num_states, self.num_actions))
        self.trans_mat = {0:-15, 1:1, 2:15, 3:-1}
        
    def get_start_state(self):
        return random.randint(0,self.num_states)
    
    def get_reward(self, prev_state, action):
        if self.prev_state + self.trans_mat[action] == (self.num_states*3/4):
            return 10
        return -1 
    
    def select_action(self, state):
        best_action = nonzero(self.Q_mat[state]==max(self.Q_mat[state]))[0]
        return best_action[random.randint(0,len(best_action))] if random.random() < .9 else random.randint(0,self.num_actions)
    
    def execute_action(self, state, action):
        move = self.trans_mat[action]
        self.prev_state = state
        r = self.get_reward(self.prev_state, action)
        self.curr_state = min(max(self.curr_state + move, 0),self.num_states-1)
        if self.prev_state % self.dimensions[0] == 0 and self.curr_state % self.dimensions[0] == 14:
            self.curr_state -= 1
        if self.prev_state % self.dimensions[0] == 14 and self.curr_state % self.dimensions[0] == 0:
            self.curr_state += 1
        self.Q_mat[self.prev_state,action] = (
            self.Q_mat[self.prev_state,action]*(1-self.alpha) +
            (r + self.gamma*max(self.Q_mat[self.curr_state]))*self.alpha)
        if r == 10:
            return True
        return False
    
    def display(self):
        fig1 = pyplot.figure(1)
        mpl_util.plot_running_average(self.tot_reward,100)
        fig1.suptitle("Rewards")
        fig2 = pyplot.figure(2)
        mpl_util.plot_running_average(self.tot_steps,100)
        fig2.suptitle("Steps")
        pyplot.show()

if __name__=="__main__":
    rl = Simple_RL(.1,.95)
    rl.run(1000)
    print rl.Q_mat