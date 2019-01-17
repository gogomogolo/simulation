import processors.Preprocessor as Preprocessor
import processors.Mainprocessor as Mainprocessor
import processors.Postprocessor as Postprocessor
import processors.FileProcessor as FileProcessor
import processors.DrawProcessor as DrawProcessor

END_DEVICE_NUMBER = 100000

MIN_SF = 7
MAX_SF = 12

EXPONENTIAL_DIST_SIZE = MAX_SF - MIN_SF + 1
EXPONENTIAL_DIST_SCALE = 1

SUPER_GROUP_LENGTH_IN_SECONDS = 15
DEVICE_ADDRESS_LENGTH_IN_BIT = 32
SUBSCRIPTION_ID_LENGTH_IN_BIT = 24

# they are for calculation of the time on air
BANDWIDTH_IN_HERTZ = 125000
NUMBER_OF_PREAMBLE = 8
SYNCHRONIZATION_WORD = 8
SF_TO_MAC_PAYLOAD_IN_BYTE = {7: 250, 8: 250, 9: 123, 10: 59, 11: 59, 12: 59}
SF_TO_SUPER_GROUP_PERIOD_IN_SEC = {7: 10800, 8: 10800, 9: 10800, 10: 10800, 11: 10800, 12: 10800}
CRC = 1
IH = 0
DE = 0
CODING_RATE = 1

DUTY_CYCLE_IN_PERCENTAGE = 1

SIMULATION_LIFE_TIME_IN_SECONDS = 86400

SF_TO_ACTIVATION_PROB = {7: 0.3, 8: 0.3, 9: 0.3, 10: 0.3, 11: 0.3, 12: 0.3}

Preprocessor.initialize(
    END_DEVICE_NUMBER
    ,MIN_SF
    ,MAX_SF
    ,SUPER_GROUP_LENGTH_IN_SECONDS
    ,DEVICE_ADDRESS_LENGTH_IN_BIT
    ,SUBSCRIPTION_ID_LENGTH_IN_BIT
    ,BANDWIDTH_IN_HERTZ
    ,NUMBER_OF_PREAMBLE
    ,SYNCHRONIZATION_WORD
    ,SF_TO_MAC_PAYLOAD_IN_BYTE
    ,SF_TO_SUPER_GROUP_PERIOD_IN_SEC
    ,CRC
    ,IH
    ,DE
    ,CODING_RATE
    ,DUTY_CYCLE_IN_PERCENTAGE
    ,SIMULATION_LIFE_TIME_IN_SECONDS
    ,SF_TO_ACTIVATION_PROB)
Mainprocessor.run()
Postprocessor.flush()
super_group_analysis = FileProcessor.get_super_group_analysis()
group_analysis = FileProcessor.get_group_analysis(super_group_analysis)
DrawProcessor.draw_group_states(group_analysis)
DrawProcessor.draw_super_group_states(group_analysis)
DrawProcessor.draw_total_all_transmission_states(group_analysis)

