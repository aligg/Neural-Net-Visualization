from MultiLinkNode import LayerType, Neurode
from FFNeurode import FFNeurode


class BPNeurode(Neurode):
    """Class responsible for handling neural network backpropagation."""

    def __init__(self, my_type):
        """BP Neurode class constructor."""
        super().__init__(my_type)
        self.delta = 0
        self.learning_rate = .05

    @staticmethod
    def sigmoid_derivative(value):
        """Outputs sigmoid fns derivative."""
        return value * (1 - value)

    def get_learning_rate(self):
        """Accessor for learning rate."""
        return self.learning_rate

    def get_delta(self):
        """Accessor for delta."""
        return self.delta

    def get_weight_for_input_node(self, from_node):
        """Accessor to return weight of from_node."""
        return self.input_nodes[from_node]

    def adjust_input_node(self, node, value):
        """Mutator that adds value to input_nodes[node]"""
        self.input_nodes[node] += value

    def receive_back_input(self, from_node=None, expected=0):
        """Accept data back from neighbor neurodes."""

        if self.register_back_input(from_node):
            self.calculate_delta(expected)
            self.back_fire()
            if self.my_type is not LayerType.OUTPUT:
                self.update_weights()

    def register_back_input(self, from_node):
        """Process outgoing data."""

        if self.my_type == LayerType.OUTPUT:
            return True

        index = 0;
        for i, k in enumerate(self.output_nodes):
            if k == from_node:
                index = i
        self.reporting_outputs = self.reporting_outputs | (1 << index)

        if self.reporting_outputs == self.compare_outputs_full:
            self.reporting_inputs = 0
            return True
        return False

    def calculate_delta(self, expected=None):
        """Helper that calculates and updates delta."""

        if self.my_type == LayerType.OUTPUT:
            self.delta = (expected - self.value) * self.sigmoid_derivative(self.value)

        elif self.my_type == LayerType.HIDDEN:
            weighted_sum = 0
            for node, _ in self.output_nodes.items():
                weight = node.get_weight_for_input_node(self)
                to_add = node.get_delta() * weight
                weighted_sum += to_add
            self.delta = weighted_sum * self.sigmoid_derivative(self.value)

    def update_weights(self):
        """Updates incoming weights."""

        for node, weight in self.output_nodes.items():
            adjustment = node.get_learning_rate() * node.get_delta() * self.value
            node.adjust_input_node(self, adjustment)

    def back_fire(self):
        """Pass data back towards input side."""

        for node in self.input_nodes:
            if node.get_type == LayerType.INPUT:
                continue
            node.receive_back_input(self)


class FFBPNeurode(FFNeurode, BPNeurode):
    """FFBPNeurode class."""

    def __init__(self, my_type):
        super().__init__(my_type)
        self.my_type = my_type

