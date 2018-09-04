from scipy.stats import bernoulli
from contracts.Distribution import Distribution


class Bernoulli(Distribution):
    def __init__(self, size, p):
        self.p = p
        self.size = size

    def sample(self):
        return bernoulli.rvs(size=self.size, p=self.p)

    def pf(self):
        return bernoulli.pmf()
