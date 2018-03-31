def prob(p, true):
    if true:
        return p
    else:
        return 1-p

def multiply(lst):
    return reduce(lambda x, y: x*y, lst)