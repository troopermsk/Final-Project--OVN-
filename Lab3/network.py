import json
from cmath import sqrt

import numpy as np

from signal import Signal_information
from line import Line
from node import Node
import matplotlib.pyplot as plt
import pandas as pd
from connection import Connection
class Network:

    def __init__(self, filename: str):
        data = json.load(open(filename, 'r'))
        self.nodes = {}
        self.lines = {}
        self.connected = False
        self._weighted_paths = None
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
                self.connected = True

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

    @property
    def weighted_paths(self):
        return self._weighted_paths

    def create_weighted_path(self, signal_power):
        node_labels = self.nodes.keys()
        pairs = []
        for label0 in node_labels:
            for label1 in node_labels:
                if label0 != label1:
                    pairs.append(label0 + label1)
        #                 we have added a pair of nodes to pairs.
        columns = ['path', 'latency', 'noise', 'snr']
        df = pd.DataFrame()
        paths_l = []
        latency_l = []
        noise_l = []
        snr_l = []
        for pair in pairs:
            for path in self.find_paths(pair[0], pair[1]):
                path_string = ''
                for node in path:
                    path_string += node + "->"
                paths_l.append(path_string[:-2])
                #             we did -2 because in the actual list of paths we dont need -> operator
                signal_info = Signal_information(signal_power, path)
                signal_info = self.propagate(signal_info)
                latency_l.append(signal_info.latency)
                noise_l.append(signal_info.noise_power)
                snr_l.append(10 * np.log10(signal_info.signal_power / signal_info.noise_power))
        df['path'] = paths_l
        df['latency'] = latency_l
        df['noise'] = noise_l
        df['snr'] = snr_l
        self._weighted_paths = df

    def find_best_snr(self, input_node, output_node):
        # all_poss_paths = self.weighted_paths.path.values
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_df = self.weighted_paths.loc[self.weighted_paths.path.isin(available_paths)]
            best_snr = np.max(inout_df.snr.values)
            best_path = inout_df.loc[inout_df.snr == best_snr].path.values[0].replace('->', '')
        else:
            best_path = None
        return best_path

    def find_best_latency(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_df = self.weighted_paths.loc[self.weighted_paths.path.isin(available_paths)]
            best_latency = np.min(inout_df.latency.values)
            best_path =  inout_df.loc[inout_df.latency == best_latency].path.values[0].replace('->', '')
        else:
            best_path = None
        return best_path

    def available_paths(self, inp_node, out_node):
        if self.weighted_paths is None:
            self.create_weighted_path(1)
        all_paths = [path for path in self.weighted_paths.path.values
                     if ((path[0] == inp_node) and (path[-1] == out_node))]
        occupied_lines = [line for line in self.lines
                          if self.lines[line].state==False]
        available_paths = []
        for path in all_paths:
            availability = True
            for line in occupied_lines:
                if line[0] + '->' + line[1] in path:
                    availability = False
                    break
            if availability:
                available_paths.append(path)
        return available_paths
    # we went through the weighted paths we were able to get with the method we previously defined
    # and checked whichever one of those were coinciding with input and outputs given in the methd
    # we also made a list of the occupied/False lines so we knew which ones to avoid

    def stream(self, connections, best='latency'):
        str_connections = []
        for connection in connections:
            inp_node = connection.input_node()
            out_node = connection.output_node()
            signal_power = connection.signal_power()
            self.create_weighted_path(1)
            if best == 'latency':
                path = self.find_best_latency(inp_node, out_node)
            elif best == 'snr':
                path = self.find_best_snr(inp_node, out_node)
            else:
                print("The best input given is not recognized. Value entered:", best)
                continue
            if path:
                inp_signal_info = Signal_information(signal_power, path)
                out_signal_info = self.propagate(inp_signal_info)
                connection._latency = out_signal_info.latency.real
                noise_power = out_signal_info.noise_power
                connection._snr = 10*np.log10(signal_power/noise_power)
                connection._snr = connection._snr.real
            else:
                connection.setLatency(None)
                connection.setSnr(0)
            str_connections.append(connection)
        return str_connections

def main():
    from random import shuffle
    network = Network('nodes.json')
    nodes = ["A", "B", "C", "D", "E", "F"]
    node_label = list(network.nodes.keys())
    connections = []
    for i in range(100):
        shuffle(node_label)
        connection = Connection(node_label[0], node_label[-1], 1e-3)
        connections.append(connection)
    streaming = network.stream(connections, best='latency')
    latencylist = [connection.latency() for connection in streaming]
    plt.hist(latencylist, bins=10)
    plt.title('The Latency Distribution')
    plt.show()
    # streaming = network.stream(connections, best='snr')
    # snrs = [connection.snr() for connection in streaming]
    # plt.hist(snrs, bins=10)
    # plt.title("The SNR Distribution")
    # plt.show()


if __name__=="__main__":
    main()
# We also need to create a Pandas dataframe with the following 'attributes' or columns, so to speak
# path strings, total accumulated latency, total accumulated noise, and signal to noise ratio.
# we can try defining some of the more specific signal related methods in the signal class so we reduce the lines added or loops added in Network class.