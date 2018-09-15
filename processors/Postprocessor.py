import parameters.Results as Results
import parameters.Constants as Constants
import time
import os


def print_results():

    with open(os.path.abspath(os.path.join('results', time.strftime("%Y%m%d-%H%M%S") + '.txt')), 'a') as result_file:
        result_file.write("*****************SIMULATION RESULTS*****************\n")
        result_file.write("\n")
        result_file.write("\n")
        result_file.write("Parameters: \n")
        result_file.write("\tEND_DEVICE_NUMBER: " + str(Constants.END_DEVICE_NUMBER) + "\n")
        result_file.write("\tMIN_SF: " + str(Constants.MIN_SF) + "\n")
        result_file.write("\tMAX_SF: " + str(Constants.MAX_SF) + "\n")
        result_file.write("\tSFs: " + str(Constants.SFs) + "\n")
        result_file.write("\tBERNOULLI_DIST_SIZE: " + str(Constants.BERNOULLI_DIST_SIZE) + "\n")
        result_file.write("\tBERNOULLI_DIST_P: " + str(Constants.BERNOULLI_DIST_P) + "\n")
        result_file.write("\tEXPONENTIAL_DIST_SIZE: " + str(Constants.EXPONENTIAL_DIST_SIZE) + "\n")
        result_file.write("\tEXPONENTIAL_DIST_SCALE: " + str(Constants.EXPONENTIAL_DIST_SCALE) + "\n")
        result_file.write("\tEND_DEVICE_MESSAGE_PERIOD: " + str(Constants.END_DEVICE_MESSAGE_PERIOD) + "\n")
        result_file.write("\tGATEWAY_MESSAGE_PERIOD: " + str(Constants.GATEWAY_MESSAGE_PERIOD) + "\n")
        result_file.write("\n")
        result_file.write("\n")
        result_file.write("Results: \n")
        result_file.write("\tNUMBER_OF_TRANSMITTERS: " + str(Results.NUMBER_OF_TRANSMITTERS) + "\n")
        result_file.write("\tNUMBER_OF_SUSPENDED_DEVICES: " + str(Results.NUMBER_OF_SUSPENDED_DEVICES) + "\n")
        result_file.write("\tNUMBER_OF_FAILED_DEVICES: " + str(Results.NUMBER_OF_FAILED_DEVICES) + "\n")
        result_file.write("\tfor same ack for all end devices scenario\n")
        result_file.write("\t\tMAC PAYLOAD OF THE GENERATED ACK: " + Results.BOOLEAN_EXP_FOR_SAME_ACK + "\n")
        result_file.write("\t\tBIT COUNT OF THE POSSIBLE DEVICE ID: " + str(Results.DEVICE_ID_LENGTH_IN_BIT_SAME_ACK) + "\n")
        result_file.write("\t\tBIT COUNT OF MAC PAYLOAD OF THE GENERATED ACK: " + str(Results.MAC_PAYLOAD_IN_BIT_SAME_ACK) + "\n")
        result_file.write("\tfor different ack for spreading factor separated devices scenario\n")
        result_file.write("\t\tMAC PAYLOAD OF THE GENERATED ACK: " + str(Results.BOOLEAN_EXP_FOR_DIFFERENT_ACK) + "\n")
        result_file.write(
            "\t\tBIT COUNT OF THE POSSIBLE DEVICE ID: " + str(Results.DEVICE_ID_LENGTH_IN_BIT_DIFFERENT_ACK) + "\n")
        result_file.write(
            "\t\tBIT COUNT OF MAC PAYLOAD OF THE GENERATED ACK: " + str(Results.MAC_PAYLOAD_IN_BIT_DIFFERENT_ACK) + "\n")
        result_file.write(
            "\t\tSPREADING FACTOR BASED NUMBER OF END DEVICES: " + str(
                Results.SPREADING_FACTOR_BASED_NUMBER_OF_END_DEVICES) + "\n")
