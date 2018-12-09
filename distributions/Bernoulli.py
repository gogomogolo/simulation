from scipy.stats import bernoulli
from contracts.Distribution import Distribution


class Bernoulli(Distribution):
    def __init__(self, size, p):
        self._bernoulli = bernoulli(p=p)
        self.size = size

    def sample(self):
        return self._bernoulli.rvs(size=self.size)

    def pf(self):
        return bernoulli.pmf()
