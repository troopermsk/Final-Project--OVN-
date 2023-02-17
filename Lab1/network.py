import json
from cmath import sqrt

import numpy as np

from signal import Signal_information
from line import Line
from node import Node
import matplotlib.pyplot as plt
import pandas as pd
class Network:

    def __init__(self, filename: str):
        data = json.load(open(filename, 'r'))
        self.nodes = {}
        self.lines = {}

        for key, value in data.items():
            dict_data = {
                "label": key,
                "position": (value["position"][0], value["position"][1]),
                "connected_nodes": value["connected_nodes"]
            }
            self.nodes[key] = Node(dict_data)
            # we get instances of the dictionary data and then we use the class constructor
#   through nodes, we can then get line.
        for value in self.nodes.values():
            for destnode in value.connected_nodes:
                # remember, line has to be between two nodes. so the value and the dest node
                # moreover in the constructor for the line, we need to put down
                self.lines[value.label + destnode] = Line(value.label + destnode, sqrt((value.position[0] - self.nodes[destnode].position[0])**2 + (value.position[1] - self.nodes[destnode].position[1])**2))
                # now we have a line added with the correct pair of letters marking starting and ending node
                # moreover, instead of having a different method for connecting them, we can try to connect them at
                # the same time when we are creating the instance.
                self.lines[value.label+destnode].connect(value, self.nodes[destnode])
                # note, we pass the value itself instead of the node because we need a dictionary of the entire class..
                # not the name only
                value.lineconnect(self.lines[value.label+destnode], destnode)

    def find_paths(self, a: str, b: str):
        path_list = []
        # we need a recursive function to go through the network.
        # for each node, look if its successive nodes has the one we want to end on
        # we need another list to store the nodes or paths that have already been taken into account
        self.find_paths_recursive(a, b, [a], path_list)
        return path_list

    def find_paths_recursive(self, a: str, b: str, traversed: list, path_list: list):
        if a == b:
            path_list.append(list(traversed))
            return
        for next_connected_node in self.nodes[a].connected_nodes:
            if next_connected_node not in traversed:
                traversed.append(next_connected_node)
                self.find_paths_recursive(next_connected_node, b, traversed, path_list)
                traversed.pop()
                # the connected path has been set so the node we were considering can now be removed.

    def propagate(self, signal: Signal_information):
        node_s = signal.update_path()
        self.nodes[node_s].propagate_method(signal)
        return signal

    def draw(self):
        node_t = self.nodes
        for label in node_t:
            n0 = node_t[label]
            x0 = node_t[label].position[0]
            y0 = node_t[label].position[1]
            plt.plot(x0, y0, 'go', markersize=12)
            plt.text(x0+15, y0+15, label)
            for connected_node_t in n0.connected_nodes:
                n1 = node_t[connected_node_t]
                x1 = n1.position[0]
                y1 = n1.position[1]
                plt.plot([x0, x1], [y0, y1], 'r')
        plt.show()
if __name__ == "main":
    net = Network("nodes.json")
    nodes = ["A", "B", "C", "D", "E", "F"]
    node_labels = net.nodes.keys()
    pairs = []
    for label0 in node_labels:
        for label1 in node_labels:
            if label0 != label1:
                pairs.append(label0+label1)
#                 we have added a pair of nodes to pairs.
    columns = ['path', 'latency', 'noise', 'snr']
    df = pd.DataFrame()
    paths_l = []
    latency_l = []
    noise_l = []
    snr_l = []
    for pair in pairs:
        for path in net.find_paths(pair[0], pair[1]):
            path_string = ''
            for node in path:
                path_string += node + "->"
            paths_l.append(path_string[:-2])
#             we did -2 because in the actual list of paths we dont need -> operator
            signal_info = Signal_information(1, path)
            signal_info = net.propagate(signal_info)
            latency_l.append(signal_info.latency)
            noise_l.append(signal_info.noise_power)
            snr_l.append(10*np.log10(signal_info.signal_power/signal_info.noise_power))
    df['path'] = paths_l
    df['latency'] = latency_l
    df['noise'] = noise_l
    df['snr'] = snr_l
# We also need to create a Pandas dataframe with the following 'attributes' or columns, so to speak
# path strings, total accumulated latency, total accumulated noise, and signal to noise ratio.
# we can try defining some of the more specific signal related methods in the signal class so we reduce the lines added or loops added in Network class.