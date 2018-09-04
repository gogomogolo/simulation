from scipy.stats import expon
from contracts.Distribution import Distribution


class Exponential(Distribution):
    def __init__(self, size, scale):
        self.size = size
        self.scale = scale

    def sample(self):
        return expon.rvs(size=self.size)

    def pf(self):
        return expon.pdf([x for x in range(0, self.size)], scale=self.scale)
