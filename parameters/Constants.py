END_DEVICE_NUMBER = 1000

MIN_SF = 7
MAX_SF = 12
SFs = [sf for sf in range(MIN_SF, MAX_SF+1)]

EXPONENTIAL_DIST_SIZE = MAX_SF - MIN_SF + 1
EXPONENTIAL_DIST_SCALE = 1

GROUP_LENGTH_IN_SECONDS = 15
DEVICE_ADDRESS_LENGTH_IN_BIT = 32
SUBSCRIPTION_ID_LENGTH_IN_BIT = 24

# they are for calculation of the time on air
BANDWIDTH_IN_HERTZ = 125
NUMBER_OF_PREAMBLE = 8
SYNCHRONIZATION_WORD = 8
SF_TO_MAC_PAYLOAD_IN_BYTE = {}
SF_TO_SUPER_GROUP_PERIOD_IN_SEC = {}
CRC = 1
IH = 0
DE = 0
CODING_RATE = 1


SF_TO_ACTIVATION_PROB = {}


# Region specific parameters

# %1
DUTY_CYCLE_IN_PERCENTAGE = 1


# Simulation life time
SIMULATION_LIFE_TIME_IN_SECONDS = 3600

LOG_FILE_DIR = ''

