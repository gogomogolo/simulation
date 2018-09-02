from contracts.BooleanExpressionMinimizer import BooleanExpressionMinimizer


class QuineMcCluskey(BooleanExpressionMinimizer):
    def __init__(self, boolean_exp, n_var):
        self.boolean_exp = boolean_exp
        self.n_var = n_var
        self.minimized_exp = []

    def minimize(self):
        print("adem")

