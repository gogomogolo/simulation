from processors.Preprocessor import initialize
from processors.Mainprocessor import run
from processors.Postprocessor import print_results

end_device_numbers = [10, 100, 1000, 10000, 100000, 1000000]


for i in end_device_numbers:
    initialize(i, 0.01, 60, 12, 7)
    run()
    print_results()
