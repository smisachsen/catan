import numpy as np

from .generate_map import get_random_map


def search_for_maps(N = 10, output = True):
    num_cities_to_check = 15 #num cities to calc mean
    city_prob_mean_treshold = 0.29 #mean of the top cities must be higher than this
    first_tenth_city_prob_diff_treshold = 0.1 #max acceptable probability diff between first and tenth city
    resource_prob_diff_treshold = 0.1 #max acceptable probability diff between the most and least likely resource

    if output:
        print("-"*20)
        print("searching for maps with N = {}" .format(N))
        print("will use num_cities = ", num_cities_to_check)
        print("first vs tenth city probability difference threshold: " .format(first_tenth_city_prob_diff_treshold))
        print("resource probability threshold: ", resource_prob_diff_treshold)
        print("-"*20)
    #todo lopp through and filter out maps that pass some test

    counter = 0
    for _ in range(N):
        map = get_random_map()

        #test of cities
        top_cities = map.city_probability_ranking[0:num_cities_to_check]
        probs = [city.probability for city in top_cities]
        #check that the mean of the top 15 probs is above some threshold
        test1 = np.mean(probs) >= city_prob_mean_treshold

        #check that the difference between the first and 10th city is less
        #than some threshold
        test2 = probs[0]-probs[10] < first_tenth_city_prob_diff_treshold
        cprobs = probs

        #test of resources
        res_probs = map.resource_probabilities
        probs = list(res_probs.values())

        #remove gold
        probs = sorted(probs)[1:]

        test3 = probs[-1] - probs[0] < resource_prob_diff_treshold

        if all([test1, test2, test3]):
            yield map
            counter += 1
