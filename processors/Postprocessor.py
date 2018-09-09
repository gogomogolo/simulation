import parameters.Results as Results


def print_results():

    print("Generated ACK in MAC Payload: " + Results.BOOLEAN_EXP_FOR_SAME_ACK)
    print("Bit count for Device Id: " + str(Results.DEVICE_ID_LENGTH_IN_BIT_SAME_ACK))
    print("Bit count for Mac Payload: " + str(Results.MAC_PAYLOAD_IN_BIT_SAME_ACK))