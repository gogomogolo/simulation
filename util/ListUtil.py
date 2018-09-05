def spread(l, value):
    if value >= 0:
        i = l.index(max(l))
        l[i] += value
    else:
        i = l.index(min(l))
        l[i] -= value
