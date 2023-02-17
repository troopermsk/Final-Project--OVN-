from cmath import log10

class Signal_information:
    def __init__(self, signal_power: float, path: list[str]):
        self.signal_power = signal_power
        self.noise_power = 0.0
        self.latency = 0.0
        self.path = list(path)

    def update_latency(self, latency:float):
        self.latency += latency

    def update_signalpower(self, signal_power: float):
        self.signal_power += signal_power

    def update_noisepower(self, noise_power: float):
        self.noise_power += noise_power

    #all the incremental methods are done.
    def update_path(self) -> str:
        if(len(self.path) > 1):
            t = self.path.pop(0)
        else:
            t = self.path[0]
        return t
    #all the setter methods are done now, we can do the Getter methods
    def get_signalpower(self):
        return self.signal_power
    def get_noisepower(self):
        return self.noise_power
    def get_latency(self):
        return self.latency
    def signal_noise_ration(self):
        return 10 * (log10(self.signal_power) - log10(self.noise_power))
    