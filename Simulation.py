import processors.Preprocessor as Preprocessor
import processors.Mainprocessor as Mainprocessor
import processors.Postprocessor as Postprocessor
import processors.FileProcessor as FileProcessor
import processors.DrawProcessor as DrawProcessor
import util.LogUtil as LogUtil

END_DEVICE_NUMBER = 5000

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
SF_TO_MAC_PAYLOAD_IN_BYTE = {7: 10, 8: 10, 9: 10, 10: 10, 11: 10, 12: 10}
SF_TO_RECEIVE_FRAME_MAC_PAYLOAD_IN_BYTE = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
SF_TO_MAX_MAC_PAYLOAD_IN_BYTE = {7: 250, 8: 250, 9: 123, 10: 59, 11: 59, 12: 59}
SF_TO_SUPER_GROUP_PERIOD_IN_SEC = {7: 3600, 8: 3600, 9: 3600, 10: 3600, 11: 3600, 12: 3600}
CRC = 1
IH = 0
DE = 0
CODING_RATE = 1

DUTY_CYCLE_IN_PERCENTAGE = 1

SIMULATION_LIFE_TIME_IN_SECONDS = 86400

SF_TO_ACTIVATION_PROB = {7: 0.5, 8: 0.1, 9: 0.1, 10: 0.9, 11: 0.9, 12: 0.9}

parameters = "\nEND_DEVICE_NUMBER = {END_DEVICE_NUMBER}\n" \
             "MIN_SF = {MIN_SF}\n" \
             "MAX_SF = {MAX_SF}\n" \
             "EXPONENTIAL_DIST_SIZE = {EXPONENTIAL_DIST_SIZE}\n" \
             "EXPONENTIAL_DIST_SCALE = {EXPONENTIAL_DIST_SCALE}\n" \
             "SUPER_GROUP_LENGTH_IN_SECONDS = {SUPER_GROUP_LENGTH_IN_SECONDS}\n" \
             "DEVICE_ADDRESS_LENGTH_IN_BIT = {DEVICE_ADDRESS_LENGTH_IN_BIT}\n" \
             "SUBSCRIPTION_ID_LENGTH_IN_BIT = {SUBSCRIPTION_ID_LENGTH_IN_BIT}\n" \
             "BANDWIDTH_IN_HERTZ = {BANDWIDTH_IN_HERTZ}\n" \
             "NUMBER_OF_PREAMBLE = {NUMBER_OF_PREAMBLE}\n" \
             "SYNCHRONIZATION_WORD = {SYNCHRONIZATION_WORD}\n" \
             "SF_TO_MAC_PAYLOAD_IN_BYTE = {SF_TO_MAC_PAYLOAD_IN_BYTE}\n" \
             "SF_TO_SUPER_GROUP_PERIOD_IN_SEC = {SF_TO_SUPER_GROUP_PERIOD_IN_SEC}\n" \
             "CRC = {CRC}\n" \
             "IH = {IH}\n" \
             "DE = {DE}\n" \
             "CODING_RATE = {CODING_RATE}\n" \
             "DUTY_CYCLE_IN_PERCENTAGE = {DUTY_CYCLE_IN_PERCENTAGE}\n" \
             "SIMULATION_LIFE_TIME_IN_SECONDS = {SIMULATION_LIFE_TIME_IN_SECONDS}\n" \
             "SF_TO_ACTIVATION_PROB = {SF_TO_ACTIVATION_PROB}\n"

LogUtil.get_file_logger('generators.SuperGroupGenerator')
LogUtil.get_file_logger('processors.Postprocessor')
LogUtil.get_file_logger('tasks.subtasks.GroupTransmissionObserver')
LogUtil.get_file_logger(__name__).info(parameters.format(
    END_DEVICE_NUMBER=END_DEVICE_NUMBER
    , MIN_SF=MIN_SF
    , MAX_SF=MAX_SF
    , EXPONENTIAL_DIST_SIZE=EXPONENTIAL_DIST_SIZE
    , EXPONENTIAL_DIST_SCALE=EXPONENTIAL_DIST_SCALE
    , SUPER_GROUP_LENGTH_IN_SECONDS=SUPER_GROUP_LENGTH_IN_SECONDS
    , DEVICE_ADDRESS_LENGTH_IN_BIT=DEVICE_ADDRESS_LENGTH_IN_BIT
    , SUBSCRIPTION_ID_LENGTH_IN_BIT=SUBSCRIPTION_ID_LENGTH_IN_BIT
    , BANDWIDTH_IN_HERTZ=BANDWIDTH_IN_HERTZ
    , NUMBER_OF_PREAMBLE=NUMBER_OF_PREAMBLE
    , SYNCHRONIZATION_WORD=SYNCHRONIZATION_WORD
    , SF_TO_MAC_PAYLOAD_IN_BYTE=SF_TO_MAC_PAYLOAD_IN_BYTE
    , SF_TO_SUPER_GROUP_PERIOD_IN_SEC=SF_TO_SUPER_GROUP_PERIOD_IN_SEC
    , CRC=CRC
    , IH=IH
    , DE=DE
    , CODING_RATE=CODING_RATE
    , DUTY_CYCLE_IN_PERCENTAGE=DUTY_CYCLE_IN_PERCENTAGE
    , SIMULATION_LIFE_TIME_IN_SECONDS=SIMULATION_LIFE_TIME_IN_SECONDS
    , SF_TO_ACTIVATION_PROB=SF_TO_ACTIVATION_PROB
))

Preprocessor.initialize(
    END_DEVICE_NUMBER
    , MIN_SF
    , MAX_SF
    , SUPER_GROUP_LENGTH_IN_SECONDS
    , DEVICE_ADDRESS_LENGTH_IN_BIT
    , SUBSCRIPTION_ID_LENGTH_IN_BIT
    , BANDWIDTH_IN_HERTZ
    , NUMBER_OF_PREAMBLE
    , SYNCHRONIZATION_WORD
    , SF_TO_MAC_PAYLOAD_IN_BYTE
    , SF_TO_RECEIVE_FRAME_MAC_PAYLOAD_IN_BYTE
    , SF_TO_MAX_MAC_PAYLOAD_IN_BYTE
    , SF_TO_SUPER_GROUP_PERIOD_IN_SEC
    , CRC
    , IH
    , DE
    , CODING_RATE
    , DUTY_CYCLE_IN_PERCENTAGE
    , SIMULATION_LIFE_TIME_IN_SECONDS
    , SF_TO_ACTIVATION_PROB)
Mainprocessor.run()
Postprocessor.flush()
super_group_analysis = FileProcessor.get_super_group_analysis()
sf_to_group_payload_analysis = FileProcessor.get_group_payload_analysis(super_group_analysis)
DrawProcessor.draw_group_payload_analysis(sf_to_group_payload_analysis)
DrawProcessor.draw_total_all_transmission_payload(sf_to_group_payload_analysis)
group_analysis = FileProcessor.get_group_analysis(super_group_analysis)
DrawProcessor.draw_group_states(group_analysis)
DrawProcessor.draw_super_group_states(group_analysis)
DrawProcessor.draw_total_all_transmission_states(group_analysis)




