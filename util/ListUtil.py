def spread(l, value):
    if value >= 0:
        i = l.index(max(l))
        l[i] += value
    else:
        i = l.index(min(l))
        l[i] -= value


def sum_list(l1, l2):
    zipped = zip(l1, l2)
    return [x+y for x, y in zipped]


def zero_list(lenth):
    return [0]*lenth

