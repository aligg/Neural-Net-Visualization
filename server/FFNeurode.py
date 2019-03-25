from MultiLinkNode import LayerType, Neurode
import numpy as np


class FFNeurode(Neurode):
    """Feed Forward Neurode, a subclass of Neurode."""

    def __init__(self, my_type):
        """Constructor for FFNeurode."""
        super().__init__(my_type)
        self.my_type = my_type

    @staticmethod
    def activate_sigmoid(value):
        """Process value using sigmoid function and return result."""
        return 1 / (1 + np.exp(-value))

    def receive_input(self, from_node=None, input_value=0):
        """Accept data from input side of the neurode."""
        if self.my_type == LayerType.INPUT:
            self.value = input_value
            [node.receive_input(self) for node in self.output_nodes]
        else:
            if self.register_input(from_node):
                self.fire()

    def register_input(self, from_node):
        """Process incoming data."""
        index = 0;
        for i, k in enumerate(self.input_nodes):
            if k == from_node:
                index = i
        self.reporting_inputs = self.reporting_inputs | (1 << index)

        if self.reporting_inputs == self.compare_inputs_full:
            self.reporting_inputs = 0
            return True
        return False

    def fire(self):
        """Calculate value of neurode and pass data to output side."""
        values = []
        [values.append(node.value * weight) for node, weight in self.input_nodes.items()]
        self.value = self.activate_sigmoid((sum(values)))
        [node.receive_input(self) for node in self.output_nodes]

