class GroupPayloadAnalysis(object):
    def __init__(self, sf, group_id, attempts, current_payloads, maximum_payload_capacities):
        self.sf = sf
        self.group_id = group_id
        self.attempts = attempts
        self.current_payloads = current_payloads
        self.maximum_payload_capacities = maximum_payload_capacities
