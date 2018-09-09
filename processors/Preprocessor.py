import parameters.Constants as Constants


def initialize(ed_n, ed_mp, gw_mp, mx_sf, mn_sf):
    Constants.END_DEVICE_NUMBER = ed_n
    Constants.MAX_SF = mx_sf
    Constants.MIN_SF = mn_sf
    Constants.END_DEVICE_MESSAGE_PERIOD = ed_mp
    Constants.GATEWAY_MESSAGE_PERIOD = gw_mp
