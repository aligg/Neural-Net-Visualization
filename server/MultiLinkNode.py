from abc import ABC, abstractmethod
from collections import OrderedDict
import random
from enum import Enum
from itertools import zip_longest


class MultiLinkNode(ABC):
    """MultiLinkNode abstract class."""

    def __init__(self, ):
        """MultiLinkNode Constructor.

            num_inputs - how many input connections
            num_outputs - how many output connections
            reporting_inputs - binary encoding of which inputs have data
            compare_inputs_full - binary encoding of what reporting inputs will look like when each input connection has data
            input_nodes = ordered dict - index (which connection node is connected to), key (node), value (data, weight of connection)
            outputs will be duplicative
        """

        self.num_inputs = 0
        self.num_outputs = 0
        self.reporting_inputs = 0
        self.reporting_outputs = 0
        self.compare_inputs_full = 0
        self.compare_outputs_full = 0
        self.input_nodes = OrderedDict()
        self.output_nodes = OrderedDict()

    @abstractmethod
    def process_new_input_node(self, node):
        """Abstract method further defined in child classes."""
        pass

    @abstractmethod
    def process_new_output_node(self, node):
        """Abstract method further defined in child classes."""
        pass

    def clear_and_add_input_nodes(self, nodes):
        """Resets input nodes and adds new."""

        self.clear_inputs()
        self.add_inputs(nodes)

    def clear_and_add_output_nodes(self, nodes):
        """Resets output nodes and adds new."""

        self.clear_outputs()
        self.add_outputs(nodes)

    def clear_inputs(self):
        """Clearing helper."""
        self.input_nodes = OrderedDict()
        self.num_inputs = 0
        self.reporting_inputs = 0
        self.compare_inputs_full = 0

    def add_inputs(self, nodes):
        """Adding helper."""
        self.input_nodes = OrderedDict(zip_longest(nodes, []))
        [self.process_new_input_node(node) for node in self.input_nodes]
        self.num_inputs = len(self.input_nodes)
        self.compare_inputs_full = self.determine_compare_full_value(self.num_inputs)
        self.reporting_inputs = self.determine_reporting_inputs(self.input_nodes)

    def clear_outputs(self):
        """Clearing helper."""
        while len(self.output_nodes) > 0:
            self.output_nodes.popitem()
        self.num_outputs = 0
        self.reporting_outputs = 0
        self.compare_outputs_full = 0

    def add_outputs(self, nodes):
        """Adding helper."""
        self.output_nodes = OrderedDict(zip_longest(nodes, []))
        [self.process_new_output_node(node) for node in self.output_nodes]
        self.num_outputs = len(self.output_nodes)
        self.compare_outputs_full = self.determine_compare_full_value(self.num_outputs)
        self.reporting_outputs = self.determine_reporting_inputs(self.output_nodes)

    @staticmethod
    def determine_compare_full_value(total):
        """Helper to calculate compare inputs and outputs full values."""
        return (1 << total) - 1

    @staticmethod
    def determine_reporting_inputs(nodes):
        """Helper to calculate reporting inputs and outputs values."""
        result = 0
        for i, (k, v) in enumerate(nodes.items()):
            if k.value:
                result = result | (1 << i)
        return result


class LayerType(Enum):
    """Enum to represent layer types for LayerList class."""
    INPUT = "input"
    HIDDEN = "hidden"
    OUTPUT = "output"


class Neurode(MultiLinkNode):
    """Neurode, a subclass of MultiLinkNode"""

    def __init__(self, my_type):
        """Constructor for Neurode.

            value - current value of the Neurode
            my_type - holds a LayerType

        """
        super().__init__()
        self.value = 0
        self.my_type = my_type

    def get_value(self):
        return self.value

    def get_type(self):
        return self.my_type

    def process_new_input_node(self, node):
        """Adds weight value between 0 & 1 to input nodes dict"""
        self.input_nodes[node] = random.random()
        return

    def process_new_output_node(self, node):
        """Placeholder method."""
        pass

