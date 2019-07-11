from scipy.stats import uniform
from contracts.Distribution import Distribution


class Uniform(Distribution):
    def __init__(self, size):
        self.size = size
        self.scale = size

    def sample(self):
        return uniform.rvs(size=self.size)

    def pf(self):
        return uniform.pdf([x for x in range(0, self.size)], scale=self.scale)
