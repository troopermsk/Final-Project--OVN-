from signal import Signal_information
#We're importing the class from the signal.py file
class Node:
    def __init__(self, inputdict: dict):
        self.label = inputdict['label']
        self.position = inputdict['position']
        self.connected_nodes = inputdict['connected_nodes']
        self.successive = {} #initialized to an empty dict
    #we have to define getters
    def get_connections(self):
        return self.connected_nodes
    def get_position(self):
        return self.position
    def propagate_method(self, signal: Signal_information):
        node = signal.update_path()
        if(node in self.connected_nodes):
            self.successive[node].propagate(signal)
    def lineconnect(self, line, destnode):
        self.successive[destnode] = line
