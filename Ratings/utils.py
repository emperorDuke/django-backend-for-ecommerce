

def calculate_avg(instance):

    """
    calculate the average rating of products or stores
    """
    
    i = instance.n_one_star_votes
    ii = instance.n_two_stars_votes
    iii = instance.n_three_stars_votes
    iv = instance.n_four_stars_votes
    v = instance.n_five_stars_votes

    n_votes = instance.n_votes

    n_stars = (i * 1) + (ii * 2) + (iii * 3) + (iv * 4) + (v * 5)

    avg = n_stars / n_votes

    return avg
