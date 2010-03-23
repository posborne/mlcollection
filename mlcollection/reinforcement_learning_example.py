'''
Created on Mar 22, 2010
@author: Zachary Varberg
'''

from numpy import *
import scipy as Sci
import scipy.linalg
import copy
import matplotlib.pyplot as pyplot

class simple_RL(object):
    
    def __init__(self, num_states, alpha, gamma, goal_state):
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.num_actions = 4
        self.Q_mat = zeros((self.num_states[0]*self.num_states[1], self.num_actions))
        self.goal_state = goal_state
        self.trans_dict={0:(0,-1),1:(1,1),2:(0,1),3:(1,-1)}
        self.start_state = [random.randint(0,num_states[0]),random.randint(0,num_states[1])]
        self.curr_state = self.start_state
        
    def execute_action(self, action):
        move = self.trans_dict[action]
        prev_state = copy.deepcopy(self.curr_state)
        self.curr_state[move[0]] = min(max(self.curr_state[move[0]] + move[1],0),self.num_states[move[0]]-1)
        r = self.get_reward(self.curr_state)
        self.Q_mat[self.num_states[0]*(prev_state[0]) + prev_state[1],action] = (
            self.Q_mat[self.num_states[0]*(prev_state[0]) + prev_state[1],action]*(1-self.alpha) +
            (r + self.gamma*max(self.Q_mat[self.num_states[0]*(self.curr_state[0]) + (self.curr_state[1])]))*self.alpha)
        if tuple(self.curr_state) == self.goal_state:
            return True
        return False
    
    def get_reward(self, state):
        if tuple(state) == self.goal_state:
            return 10
        return -1
    
    def run(self, num_trials):
        tot_reward = []
        tot_steps = []
        tri_reward = 0
        num_steps = 0
        for x in xrange(num_trials):
            if x%10==0 and x>=10:
                print 'Trial',x,(sum(tot_reward[x-10:x])/10),(sum(tot_steps[x-10:x])/10)
            self.curr_state = [random.randint(0,self.num_states[0]),random.randint(0,self.num_states[1])]
            #self.curr_state = [0,0]
            tri_reward = 0
            num_steps = 0
            not_done = True
            path = []
            while(not_done):
                num_steps+=1
                best_action = nonzero(self.Q_mat[self.num_states[0]*(self.curr_state[0]) + (self.curr_state[1])]==max(self.Q_mat[self.num_states[0]*(self.curr_state[0]) + (self.curr_state[1])]))[0]
                next_action = best_action[random.randint(0,len(best_action))] if random.random() <.9 else random.randint(0,self.num_actions)
                not_done = not self.execute_action(next_action)
                tri_reward += self.get_reward(self.curr_state)
                path.append(copy.deepcopy(self.curr_state))
            tot_reward.append(tri_reward)
            tot_steps.append(num_steps)
        fig1 = pyplot.figure(1)
#        pyplot.plot(xrange(num_trials),[(sum(tot_reward[x-100:x])/100) if x >=100 else (sum(tot_reward[0:x])/x) for x in xrange(num_trials)],'r--',xrange(num_trials),[(sum(tot_steps[x-100:x])/100) if x >=100 else (sum(tot_steps[0:x])/x) for x in xrange(num_trials)],'b--')
        pyplot.plot([(sum(tot_reward[x-100:x])/100) if x >=100 else (sum(tot_reward[0:x])/x) for x in xrange(num_trials)])
        fig1.suptitle("Rewards")
        fig2 = pyplot.figure(2)
        pyplot.plot([(sum(tot_steps[x-100:x])/100) if x >=100 else (sum(tot_steps[0:x])/x) for x in xrange(num_trials)])
        fig2.suptitle("Steps")
        pyplot.show()

if __name__ == "__main__":
    rl = simple_RL((25,25),.05,.95,(7,6))
    rl.run(1000)
    print rl.Q_mat
    