class GroupAnalysis(object):
    def __init__(self, sf, id, device_amount, attempts, idles, successes, fails):
        self.sf = sf
        self.id = id
        self.device_amount = device_amount
        self.attempts = attempts
        self.idles = idles
        self.successes = successes
        self.fails = fails
