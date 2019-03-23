class LorawanResults(object):
    def __init__(self, succeeded_t, failed_t, banned_t, out_of_simulation_t):
        self.succeeded_t = succeeded_t
        self.failed_t = failed_t
        self.banned_t = banned_t
        self.out_of_simulation_t = out_of_simulation_t
