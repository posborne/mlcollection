"""Base classes which other collaborative filters build upon"""

class AbstractCollaborativeFilter(object):
    
    def __init__(self, ranked_dataset=None):
        self.ranked_dataset = ranked_dataset
