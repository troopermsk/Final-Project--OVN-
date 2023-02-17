class Connection:
    def __init__(self, input_node, output_node, signal_power):
        self._inp_node = input_node
        self._out_node = output_node
        self._sig_power = signal_power
        self._latency = 0
        self._snr = 0

    def input_node(self):
        return self._inp_node
    def output_node(self):
        return self._out_node
    def signal_power(self):
        return self._sig_power
    def latency(self):
        return self._latency
    def snr(self):
        return self._snr
    def setLatency(self, latency : float):
        self._latency = latency
    def setSnr(self, snr : float):
        self._snr = snr