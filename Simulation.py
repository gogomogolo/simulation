import parameters.Constants as Constants

from processors.Preprocessor import initialize
from processors.Mainprocessor import run
from processors.Postprocessor import print_results


initialize(1000, 0.1, 60, 12, 7)
run()
print_results()
