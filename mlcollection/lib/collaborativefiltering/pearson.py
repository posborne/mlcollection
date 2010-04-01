"""Implementation of Pearson collaborative filtering algorithm"""
from math import sqrt, pow
from mlcollection.lib.collaborativefiltering.collaborativefilterbase import \
    AbstractCollaborativeFilter
from operator import itemgetter
from scipy import stats, isnan

__author__ = 'Paul Osborne <osbpau@gmail.com>'

class PearsonCollaborativeFilter(AbstractCollaborativeFilter):
    """Filter based on the Pearson correlation score between items/individuals
    
    The Pearson correlation score or coefficient is a measure of how well two
    sets of data fit onto a straight line.  There is some added complexity
    when compared to the Euclidean filtering algorithm, but the Pearson
    algorithm does a better job of dealing with data which is not normalized.
    
    An example where data is not normalized might be examining movie reviews.
    It may be the case that some reviewers are just more harsh than other
    reviewers.  In this case we cannot just draw conclusions about shared
    interest based on the score, we need to look a bit deeper to see if there
    really is a correlation between the preferences of these two people.
    
    The Pearson algorithm, when finding the similarity between two inviduals,
    first finds the subset of data that the two members have each rated/scored.
    Then, the score is calculated (using some statistics) based on the sum of
    the squares of the ratings and the sum of the products of the ratings.
    
    The formula for pearson's product-moment coefficent is as follows:
    .. math::
       
       \rho_{X,Y}={\mathrm{cov}(X,Y) \over \sigma_X \sigma_Y} ={E[(X-\mu_X)(Y-\mu_Y)] \over \sigma_X\sigma_Y}
       
    which in the statistics world is often just referred to as `corr(x,y)`.
    """
    
    def __init__(self, ranked_dataset=None):
        AbstractCollaborativeFilter.__init__(self, ranked_dataset)
    
    def get_recommendations(self, individual):
        """Find recommendedations for this individual
        
        Given the individual return a dictionary where the keys are the items
        and the values are ratings for the movie for the individual.  The
        higher the rating, the more likely it is that the individual may like
        the movie.
        """
        dataset = self.ranked_dataset
        totals = {}
        sim_sums = {}
        ind_items = set(dataset[individual].keys())
        for other in (x for x in dataset if x != individual):
            shared_items = ind_items & set(dataset[other].keys())
            
            # get a measure of how similar individual and other are
            if len(shared_items) == 0:
                continue
            x = [dataset[individual][i] for i in shared_items]
            y = [dataset[other][i] for i in shared_items]
            coeff = stats.pearsonr(x, y)[0]
            
            if coeff < 0 or isnan(coeff):
                continue

            for item in set(dataset[other]) - ind_items:
                if not item in sim_sums:
                    sim_sums[item] = 0
                    totals[item] = 0
                
                sim_sums[item] += coeff * dataset[other][item]
                totals[item] += coeff
        
        rankings = {}
        for item in totals:
            rankings[item] = sim_sums[item] / totals[item]
        return rankings