'''
Created on Mar 29, 2010

@author: Zachary Varberg
'''

from matplotlib import pyplot

def plot_running_average(my_list, ave_length):
    pyplot.plot([(sum(my_list[x-ave_length:x])/ave_length) if x >=ave_length else (sum(my_list[0:x])/x) for x in xrange(1,len(my_list))])