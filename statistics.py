def list_by_rating(books):
    return sorted(books, key = lambda x : x[1])


def n_sold_by_genre(ratings_by_genre):
    # [(genre, [books,...]), ...]
    return [(genre, sum(ratings)) for genre, ratings in ratings_by_genre]