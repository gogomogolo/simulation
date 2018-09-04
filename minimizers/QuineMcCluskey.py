from contracts.BooleanExpressionMinimizer import BooleanExpressionMinimizer
from quine_mccluskey.qm import QuineMcCluskey


class QuineMcCluskey(BooleanExpressionMinimizer):
    def __init__(self, boolean_exp):
        self.boolean_exp = boolean_exp
        self.minimized_exp = []

    def minimize(self):
        self.minimized_exp = QuineMcCluskey.simplify(ones=self.boolean_exp)
        return self.minimized_exp
