from contracts.BooleanExpressionMinimizer import BooleanExpressionMinimizer
from quine_mccluskey.qm import QuineMcCluskey


class QMC(BooleanExpressionMinimizer):
    def __init__(self, boolean_exp):
        self.boolean_exp = boolean_exp
        self.minimized_exp = []

    def minimize(self):
        qmc = QuineMcCluskey()
        self.minimized_exp = qmc.simplify(ones=self.boolean_exp)
        return self.minimized_exp
