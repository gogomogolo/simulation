import parameters.Constants as Constants

from generators.EndDeviceDistributor import distribute
from distributions.Exponential import Exponential


Constants.END_DEVICE_NUMBER = 100

distribute(Exponential(6, 8))


Constants.END_DEVICE_NUMBER = 10


distribute(Exponential(6, 8))
