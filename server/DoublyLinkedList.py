class DLLNode:
    """ Node class for a doubly linked list."""

    def __init__(self):
        self.next = None
        self.prev = None

    def set_next(self, next_node):
        self.next = next_node

    def get_next(self):
        return self.next

    def set_prev(self, prev_node):
        self.prev = prev_node

    def get_prev(self):
        return self.prev


class DoublyLinkedList:
    """
        class for a doubly linked list.

        self.head = first node in list
        self.tail = last node in list

    """

    def __init__(self):
        self.head = None
        self.current = None
        self.tail = None

    def reset_cur(self):
        self.current = self.head
        return self.current

    def iterate(self):
        if self.current is not None:
            self.current = self.current.get_next()
            return self.current

    def rev_iterate(self):
        if self.current is not None:
            self.current = self.current.get_prev()
            return self.current

    def add_to_head(self, new_node):
        """Add a node to the head."""
        if isinstance(new_node, DLLNode):
            if self.is_empty():
                self.tail = new_node

            else:
                self.head.set_prev(new_node)
            new_node.set_next(self.head)
            new_node.set_prev(None)
            self.head = new_node

    def remove_from_head(self):
        """Remove a node from head."""

        ret_node = self.head

        if ret_node == self.current:
            self.current = None

        if ret_node is None:  # empty list
            return ret_node
        self.head = ret_node.get_next()

        if self.head is not None:
            self.head.set_prev(None)
        else:  # after removal, empty list
            self.tail = None

        return ret_node

    def insert_after_cur(self, new_node):
        if isinstance(new_node, DLLNode) and self.current:
            if self.tail == self.current:
                self.tail = new_node
            else:
                self.current.get_next().set_prev(new_node)
            new_node.set_next(self.current.get_next())
            new_node.set_prev(self.current)
            self.current.set_next(new_node)
            return True
        else:
            return False

    def remove_after_cur(self):
        if not self.current or not self.current.get_next():
            return False
        if self.current.get_next() == self.tail:
            self.tail = self.current

        skip_node = self.current.get_next().get_next()
        self.current.set_next(skip_node)
        if skip_node is not None:
            skip_node.set_prev(self.current)

    def is_empty(self):
        return self.head is None

