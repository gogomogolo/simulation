import parameters.Constants as Constants
import parameters.Results as Results
from random import randrange


def initialize(ed_n, ed_mp, gw_mp, mx_sf, mn_sf, gid_len):
    Constants.END_DEVICE_NUMBER = ed_n
    Constants.MAX_SF = mx_sf
    Constants.MIN_SF = mn_sf
    Constants.END_DEVICE_MESSAGE_PERIOD = ed_mp
    Constants.GATEWAY_MESSAGE_PERIOD = gw_mp
    Constants.SFs = [sf for sf in range(Constants.MIN_SF, Constants.MAX_SF + 1)]
    Constants.BERNOULLI_DIST_SIZE = Constants.END_DEVICE_NUMBER
    Constants.BERNOULLI_DIST_P = float(randrange(1, 10)) / (float(Constants.END_DEVICE_NUMBER))
    Constants.EXPONENTIAL_DIST_SIZE = Constants.MAX_SF - Constants.MIN_SF + 1
    Constants.EXPONENTIAL_DIST_SCALE = 1
    Constants.GROUP_ID_LENGTH_IN_BIT = gid_len

    Results.BOOLEAN_EXP_FOR_SAME_ACK = ''
    Results.DEVICE_ID_LENGTH_IN_BIT_SAME_ACK = 0
    Results.MAC_PAYLOAD_IN_BIT_SAME_ACK = 0
    Results.BOOLEAN_EXP_FOR_DIFFERENT_ACK = {}
    Results.DEVICE_ID_LENGTH_IN_BIT_DIFFERENT_ACK = {}
    Results.MAC_PAYLOAD_IN_BIT_DIFFERENT_ACK = {}
    Results.SPREADING_FACTOR_BASED_NUMBER_OF_END_DEVICES = {}
    Results.NUMBER_OF_TRANSMITTERS = 0
    Results.NUMBER_OF_SUSPENDED_DEVICES = 0
    Results.NUMBER_OF_FAILED_DEVICES = 0

