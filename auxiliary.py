import math

def prob(p, true):
    if true:
        return p
    else:
        return 1-p

def multiply(lst):
    return reduce(lambda x, y: x*y, lst)

def avg_of_abs_diffs(dict1, dict2):
    return sum([math.fabs(dict1[key]-dict2[key]) for key in dict1])/len(dict1)