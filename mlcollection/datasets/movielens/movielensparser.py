"""Parser and data classes for easily accessing movielens dataset

.. note::
   The dataset is fairly large (100,000 ratings plus extra metadata) and the
   parser currently loads this all into memory.  Computers these days seem to
   handle this, just be aware that it isn't exactly trim when loaded in and
   you probably don't want to have too many of these guys laying around.
"""
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILE = os.path.join(THIS_DIR, 'u.data')
GENRE_FILE = os.path.join(THIS_DIR, 'u.genre')
ITEM_FILE = os.path.join(THIS_DIR, 'u.item')
OCCUPATION_FILE = os.path.join(THIS_DIR, 'u.occupation')
USER_FILE = os.path.join(THIS_DIR, 'u.user')

__author__ = 'Paul Osborne <osbpau@gmail.com>'

class MovieLensParser(object):
    """Parser for movielens data set
    
    Since the dataset is quite large, some of the data we cache in memory
    up front, and other we iterate over our open file handles (e.g. the data).
    """
    
    def __init__(self):
        # Initialize the parser
        self.genre_by_id = self._parse_genre()
        self.user_by_id = self._parse_user()
        self.movies_by_id = self._parse_movies()
        self.ratings_by_userid, self.ratings_by_movieid = self._parse_ratings()
    
    def _parse_user(self):
        users_by_id = {}
        with open(USER_FILE) as user_file:
            for line in user_file:
                line = line.strip()
                if line:
                    user = MovieLensUser(*tuple(line.split('|')))
                    users_by_id[user.id] = user
        return users_by_id
    
    def _parse_genre(self):
        # pull out genre mapping
        genre_map = {}
        with open(GENRE_FILE) as genre_file:
            for line in genre_file:
                line = line.strip()
                if line:
                    genre, genre_id = line.split('|')
                    genre_map[genre_id] = genre
        return genre_map

    def _parse_movies(self):
        # parse the movie information out
        movies = {}
        with open(ITEM_FILE) as item_file:
            for line in item_file:
                line = line.strip()
                if line:
                    items = tuple(line.split('|'))
                    movie = MovieLensMovie(*items)
                    movies[movie.id] = movie
        return movies

    def _parse_ratings(self):
        ratings_by_userid = {}
        ratings_by_movieid = {}
        with open(DATA_FILE, 'r') as data_file:
            for line in data_file:
                line.strip()
                if line:
                    rating = MovieLensRating(*tuple(line.split()))
                    ratings_by_userid.setdefault(rating.user_id, set())
                    ratings_by_movieid.setdefault(rating.movie_id, set())
                    ratings_by_userid[rating.user_id].add(rating)
                    ratings_by_movieid[rating.movie_id].add(rating)
        return ratings_by_userid, ratings_by_movieid

class MovieLensRating(object):
    """Encapsulate movie rating data"""
    
    def __init__(self, user_id, movie_id, rating, timestamp):
        self.user_id = int(user_id)
        self.movie_id = int(movie_id)
        self.rating = int(rating)
        self.timestamp = int(timestamp)
    
    def __eq__(self, other):
        return (isinstance(other, MovieLensRating) and
                self.user_id, self.movie_id, self.rating, self.timestamp ==
                other.user_id, other.movie_id, other.rating, other.timestamp)
    
    def __hash__(self):
        return hash((self.user_id, self.movie_id, self.rating, self.timestamp,))
    

class MovieLensUser(object):
    """Encapsulate data about a movielens user"""
    
    def __init__(self, id, age, gender, occupation, zipcode):
        self.id = int(id)
        self.age = int(age)
        self.gender = gender
        self.occupation = occupation
        self.zipcode = zipcode

    def __eq__(self, other):
        return isinstance(other, MovieLensUser) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

class MovieLensMovie(object):
    """Encapsulate data about a movielens movie"""
    
    GENRE_KEYS = ('action',
                  'adventure',
                  'animation',
                  'childrens',
                  'comedy',
                  'crime',
                  'crime',
                  'documentary',
                  'musical',
                  'mystery',
                  'romance',
                  'scifi',
                  'thriller',
                  'war',
                  'western',
                  'unknown',)
    
    def __init__(self, movie_id, title, release_date, video_release_date, imdb_url,
                 action, unknown, adventure, animation, childrens, comedy, crime,
                 documentary, drama, fantasy, film_noir, horror, musical,
                 mystery, romance, scifi, thriller, war, western):
        self.id = int(movie_id)
        self.title = title
        self.release_date = release_date
        self.video_release_date = video_release_date
        self.imdb_url = imdb_url
        self.unknown = self._bool_map(unknown)
        self.action = self._bool_map(action)
        self.adventure = self._bool_map(adventure)
        self.animation = self._bool_map(animation)
        self.childrens = self._bool_map(childrens)
        self.comedy = self._bool_map(comedy)
        self.crime = self._bool_map(crime)
        self.documentary = self._bool_map(documentary)
        self.drama = self._bool_map(drama)
        self.fantasy = self._bool_map(fantasy)
        self.film_noir = self._bool_map(film_noir)
        self.horror = self._bool_map(horror)
        self.musical = self._bool_map(musical)
        self.mystery = self._bool_map(mystery)
        self.romance = self._bool_map(romance)
        self.scifi = self._bool_map(scifi)
        self.thriller = self._bool_map(thriller)
        self.war = self._bool_map(war)
        self.western = self._bool_map(western)
        self.genres = self._create_genre_set()
    
    def _bool_map(self, val):
        return (val == True or val == 1 or val == '1')

    def _create_genre_set(self):
        # create set of genres
        genres = set()
        for genre in self.GENRE_KEYS:
            if getattr(self, genre):
                genres.add(genre)
    
    def __eq__(self, other):
        return isinstance(other, MovieLensMovie) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

if __name__ == '__main__':
    parser = MovieLensParser()
    for rating in parser.ratings_by_userid[35]:
        print rating.movie_id, parser.movies_by_id[rating.movie_id].title
