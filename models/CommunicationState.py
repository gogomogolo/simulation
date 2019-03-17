import parameters.Constants as Constants
import util.LorawanUtil as LorawanUtil


class CommunicationState(object):
    def __init__(self, sf, transmitted_message_toa, time_slot, end_devices):
        self.sf = sf
        self.is_collision = len(end_devices) > 1
        self.end_devices = end_devices

        self.transmitted_message_toa = transmitted_message_toa
        self.transmission_time = float(transmitted_message_toa * time_slot)
        self.end_of_transmission_time = float(transmitted_message_toa * time_slot) + transmitted_message_toa
        self.transmission_time_slot = time_slot

        self.receiving_message_toa = self.get_time_on_air_for_receiving_messages(sf)
        self.first_receive_window_time = float(transmitted_message_toa * (time_slot + 1) + 1)
        self.first_receive_window_time_slot = int(float(transmitted_message_toa * (time_slot + 1) + 1)/transmitted_message_toa)
        self.second_receive_window_time = float(transmitted_message_toa * (time_slot + 1) + 1) + self.receiving_message_toa
        self.second_receive_window_time_slot = int((float(transmitted_message_toa * (time_slot + 1) + 1) +
                                                     self.receiving_message_toa)/transmitted_message_toa)

    def get_time_on_air_for_receiving_messages(self, sf):
        return LorawanUtil.calculate_time_on_air(
            Constants.BANDWIDTH_IN_HERTZ,
            Constants.NUMBER_OF_PREAMBLE,
            Constants.SYNCHRONIZATION_WORD,
            Constants.SF_TO_RECEIVE_FRAME_MAC_PAYLOAD_IN_BYTE[sf],
            sf,
            Constants.CRC,
            Constants.IH,
            Constants.DE,
            Constants.CODING_RATE)

