"""
Assignment Eight
Ali Glenesk
"""
from BPNeurode import FFBPNeurode
from DoublyLinkedList import DLLNode
from MultiLinkNode import LayerType
from DoublyLinkedList import DoublyLinkedList


class NodePositionError(Exception):
    """Class to handle raising error in case of node positioning error."""
    pass


class Layer(DLLNode):
    """Handles functionality for Neural Net."""

    def __init__(self, num_neurodes=5, my_type=LayerType.HIDDEN):
        """Layer constructor."""
        self.my_type = my_type
        self.num_neurodes = num_neurodes
        self.neurodes = []
        for _ in range(num_neurodes):
            self.add_neurode()

    def add_neurode(self):
        """Method for adding neurodes to the layer."""
        new_neurode = FFBPNeurode(self.my_type)
        self.neurodes.append(new_neurode)

    def get_my_neurodes(self):
        """Accessor for list of neurodes."""
        return self.neurodes

    def get_my_type(self):
        """Accessor for type of this layer."""
        return self.my_type

    def get_layer_info(self):
        """Returns tuple of layer type and num neurodes."""
        return self.my_type, self.num_neurodes


class LayerList(DoublyLinkedList):
    """Class to handle adding and removing hidden layers."""

    def __init__(self, num_inputs, num_outputs):
        """LayerList constructor."""
        super().__init__()

        self.input_layer = Layer(num_inputs, LayerType.INPUT)
        self.output_layer = Layer(num_outputs, LayerType.OUTPUT)

        # add input layer to list using add_to_head
        self.add_to_head(self.input_layer)
        # add output layer to list using insert_after_cur
        self.current = self.head
        self._insert_after_cur(self.output_layer)
        # remember, current needs to be pointing somewhere rational

    def _insert_after_cur(self, new_layer):
        """Method to format up layer obj and its neurodes then insert. """
        for neurode in self.current.get_my_neurodes():
            neurode.clear_outputs()
            neurode.add_outputs(new_layer.get_my_neurodes())
        for neurode in new_layer.get_my_neurodes():
            neurode.add_inputs(self.current.get_my_neurodes())

        if new_layer.get_my_type() is LayerType.HIDDEN:
            if self.current.get_next():
                for neurode in new_layer.get_my_neurodes():
                    neurode.add_outputs(self.current.get_next().get_my_neurodes())
                for neurode in self.current.get_next().get_my_neurodes():
                    neurode.clear_inputs()
                    neurode.add_inputs(new_layer.get_my_neurodes())

        super().insert_after_cur(new_layer)

    def _remove_after_cur(self):
        """Method to prepare hidden layer for removal then remove."""

        node_to_remove = self.current.get_next()

        # delink neurodes in the layer we want to remove
        for neurode in node_to_remove.get_my_neurodes():
            neurode.clear_inputs()
            neurode.clear_outputs()
        # make sure remaining layers' neurodes are appropriately linked
        if node_to_remove.get_next():
            for neurode in self.current.get_my_neurodes():
                neurode.clear_outputs()
                neurode.add_outputs(node_to_remove.get_next().get_my_neurodes())
            for neurode in node_to_remove.get_next().get_my_neurodes():
                neurode.clear_inputs()
                neurode.add_inputs(self.current.get_my_neurodes())
        super().remove_after_cur()

    def insert_hidden_layer(self, num_neurodes):
        # create and add a hidden layer with appropriate num of neurodes
        hidden_layer = Layer(num_neurodes)

        # if self.current pointing to tail then raise node position error
        if self.current == self.tail:
            raise NodePositionError
        # then add it after self.current
        self._insert_after_cur(hidden_layer)

    def remove_hidden_layer(self):
        # remove the layer after self.current
        next_node = self.current.get_next()
        if next_node.my_type is not LayerType.HIDDEN:
            raise NodePositionError
        # call remove_after_curr
        self._remove_after_cur()

    def get_input_nodes(self):
        """Returns list of nodes at the head."""
        return self.head.get_my_neurodes()

    def get_output_nodes(self):
        """Returns list of nodes at the tail."""
        return self.tail.get_my_neurodes()

