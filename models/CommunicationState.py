import parameters.Constants as Constants
import util.LorawanUtil as LorawanUtil


class CommunicationState(object):
    def __init__(self, sf, transmitted_message_toa, time_slot, observation_start_t, end_devices):
        self.sf = sf
        self.is_collision = len(end_devices) > 1
        self.end_devices = end_devices

        self.transmitted_message_toa = transmitted_message_toa
        self.transmission_time = observation_start_t + float(transmitted_message_toa * time_slot)
        self.end_of_transmission_time = observation_start_t + float(transmitted_message_toa * time_slot) + transmitted_message_toa

        self.receiving_message_toa = self.get_time_on_air_for_receiving_messages(sf)
        self.first_receive_window_time = observation_start_t + float(transmitted_message_toa * (time_slot + 1) + 1)
        self.second_receive_window_time = observation_start_t + float(transmitted_message_toa * (time_slot + 1) + 1) + self.receiving_message_toa

        self.will_be_active_transmission_time = self.transmission_time + \
                                              (transmitted_message_toa * float(
                                            100 / Constants.DUTY_CYCLE_IN_PERCENTAGE))

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

