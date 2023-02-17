from node import Node
from signal import Signal_information

class Line:

    def __init__(self, label, length):
        self.label = label
        self.length = length
        self.successive = {}
        self.state = "free"

    def get_label(self):
        return self.label

    def get_length(self):
        return self.length

    def latency_generation(self):
        speed = 2/3 *3*10**8
        return self.length/speed
# distance divided by time for the latency time delay
    def noise_generation(self, signal_power : float):
        return 1e-9*signal_power * self.length

    def propagate(self, signal: Signal_information):
        signal.update_noisepower(self.noise_generation(signal.get_signalpower()))
        signal.update_latency(self.latency_generation())
        self.successive["destnnode"].propagate_method(signal)
    #     we have in the above three lines, updated noise power, latency,
    # and the state of the signal respectively

    def connect(self, startnode, destnode):
        self.successive["startnode"] = startnode
        self.successive["destnnode"] = destnode
        # each line has a dict of nodes which are successive to it
    def occupy(self):
        if(self.state):
            self.state = False
            return True
        return False
    def free(self):
        if (not self.state):
            self.state = True









