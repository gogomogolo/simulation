class EndDevice(object):
    def __init__(self, _id, _sf):
        self._id = _id
        self._sf = _sf
        self.transmission_status = "NONE"
        self.transmitting_attempt = 0
        self.retransmitting_attempt = 0

    def set_transmission_status(self, status):
        self.transmission_status = status

    def set_transmitting_attempt(self, attempt):
        self.transmitting_attempt = attempt

    def set_retransmitting_attempt(self, attempt):
        self.retransmitting_attempt = attempt
