import math


def calculate_symbol_duration(sf, bw_in_hz):
    return (2**sf) / bw_in_hz


def calculate_preamble_symbol(np):
    return 4.25 + np


def calculate_packet_symbol(sw, pl, sf, crc, ih, de, cr):
    return sw + max(math.ceil((8 * pl - 4 * sf + 28 + 16 * crc - 20 * ih) / (4 * (sf - 2 * de))) * (cr + 4), 0)


def calculate_time_on_air(bw_in_hz, np, sw, pl, sf, crc, ih, de, cr):
    return calculate_symbol_duration(sf, bw_in_hz) * (calculate_preamble_symbol(np) *
                                                      calculate_packet_symbol(sw, pl, sf, crc, ih, de, cr))



