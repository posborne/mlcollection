from mlcollection.datasets.movielens.movielensparser import MovieLensParser
from mlcollection.lib.collaborativefiltering import pearson
from operator import itemgetter

class MovieRecommender(MovieLensParser):
     
    def __init__(self):
        # this will load in our data set
        MovieLensParser.__init__(self)
        
    def movie_recommendations(self, individual_id):
        ranked_dataset = {}
        for user_id, ratingset in self.ratings_by_userid.iteritems():
            ranked_dataset.setdefault(user_id, {})
            ranked_dataset[user_id] = dict([(r.movie_id, r.rating) for r in ratingset])
        
        filter = pearson.PearsonCollaborativeFilter(ranked_dataset)
        recommendations = filter.get_recommendations(individual_id)
        return recommendations

if __name__ == '__main__':
    user_id = int(raw_input("Enter User Id: "))
    rec = MovieRecommender()
    user = rec.user_by_id[user_id]
    recommendations = rec.movie_recommendations(user_id)
    print "== User: %s, %s, %s, %s ==" % (user.id, user.age, user.gender, user.occupation)
    for i, (movie_id, score) in enumerate(list(reversed(sorted(recommendations.iteritems(), key=itemgetter(1))))[:20]):
        movie = rec.movies_by_id[movie_id]
        print "* (#%d @ %s) - Movie: %s" % (movie_id, score, movie.title)
