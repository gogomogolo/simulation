import processors.Preprocessor as Preprocessor
import processors.Mainprocessor as Mainprocessor
import processors.Postprocessor as Postprocessor
import processors.ShellProcessor as ShellProcessor
import util.LogUtil as LogUtil
import parameters.Constants as Constants
import MathematicalModel as mm


def simulation(SF_TO_MAC_PAYLOAD_IN_BYTE, END_DEVICE_NUMBER, SF_TO_SUPER_GROUP_PERIOD_IN_SEC, SIMULATION_LIFE_TIME_IN_SECONDS):
    MIN_SF = 7
    MAX_SF = 12

    EXPONENTIAL_DIST_SIZE = MAX_SF - MIN_SF + 1
    EXPONENTIAL_DIST_SCALE = 2

    SUPER_GROUP_LENGTH_IN_SECONDS = 15
    DEVICE_ADDRESS_LENGTH_IN_BIT = 32
    SUBSCRIPTION_ID_LENGTH_IN_BIT = 24

    # they are for calculation of the time on air
    BANDWIDTH_IN_HERTZ = 125000
    NUMBER_OF_PREAMBLE = 8
    SYNCHRONIZATION_WORD = 8
    SF_TO_RECEIVE_FRAME_MAC_PAYLOAD_IN_BYTE = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    SF_TO_MAX_MAC_PAYLOAD_IN_BYTE = {7: 250, 8: 250, 9: 123, 10: 59, 11: 59, 12: 59}

    CRC = 1
    IH = 0
    DE = 0
    CODING_RATE = 1

    DUTY_CYCLE_IN_PERCENTAGE = 1
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

    LogUtil.init_logutil()
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
    Postprocessor.networkLoad(Constants.LOG_FILE_DIR)
    ShellProcessor.get_report()
    mm.compareResultWithModel(Constants.LOG_FILE_DIR)
    simulation_results_dir = Constants.LOG_FILE_DIR
    LogUtil.reset()

    return simulation_results_dir




