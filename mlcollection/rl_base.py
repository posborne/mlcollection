'''
Created on Mar 23, 2010

@author: Zachary Varberg
'''

from numpy import *
import scipy as Sci
import scipy.linalg
import copy
import matplotlib.pyplot as pyplot

class Base_RL(object):
    
    def __init__(self):
        self.start_state = None
        self.curr_state = None
        self.prev_state = None
        self.num_states = None
        pass
    
    def execute_action(self, state, action):
        '''
        This is expected to return True if the trial has terminated and false
        otherwise
        '''
        raise NotImplementedError( "This must be implemented by the child class of Base_RL" )
    
    def get_reward(self, state, action):
        ''' 
        This returns an int that is the value of taking the given action in the
        given state
        '''
        raise NotImplementedError( "This must be implemented by the child class of Base_RL" )
    
    def display(self):
        ''' 
        This should display the results on a graph
        '''
        raise NotImplementedError( "This must be implemented by the child class of Base_RL" )
    
    def select_action(self, curr_state):
        ''' 
        This should return the next action to take from the given state
        '''
        raise NotImplementedError( "This must be implemented by the child class of Base_RL" )
    
    def get_start_state(self):
        ''' 
        This should return a start state for a trial, whether it is random or a 
        static state.
        '''
        raise NotImplementedError( "This must be implemented by the child class of Base_RL" )
    
    def run(self, num_trials):
        self.num_trials = num_trials
        self.tot_reward = []
        self.tot_steps = []
        tri_reward = 0
        num_steps = 0
        for x in xrange(num_trials):
            if x%10==0 and x>=10:
                print 'Trial',x
            self.curr_state = self.get_start_state()
            tri_reward = 0
            num_steps = 0
            not_done = True
            #path = []
            while(not_done):
                num_steps+=1
                next_action = self.select_action(self.curr_state)
                not_done = not self.execute_action(self.curr_state, next_action)
                tri_reward += self.get_reward(self.prev_state, next_action)
                #path.append(copy.deepcopy(self.curr_state))
            self.tot_reward.append(tri_reward)
            self.tot_steps.append(num_steps)
        self.display()
