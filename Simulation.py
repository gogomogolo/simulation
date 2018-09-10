import parameters.Constants as Constants

from processors.Preprocessor import initialize
from processors.Mainprocessor import run
from processors.Postprocessor import print_results


initialize(10000, 0.01, 60, 12, 7)
run()
print_results()
