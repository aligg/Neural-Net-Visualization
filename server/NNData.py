
"""
Assignment2
Ali Glenesk
"""
import random
from collections import deque
from enum import Enum


class DataMismatchError(Exception):
    """Class to handle raising errors if set sizes do not match."""
    pass


class NNData(object):
    """Class for Neural Network Data."""

    def __init__(self, x=None, y=[], percentage: int = 100):
        """Constructor for NNData object.

            x example part of data we want loaded, list of lists
            y label part of data we want loaded, list of lists
            percentage is an int representing the portion of data we want used as our training set
            train_indices list of pointers to training subset
            train_pool deque containing ex not yet used in curr epoch
            test_indices pointers to testing subset of data, list
            test_pool deque containing ex not yet used in curr run
        """
        self.x = x
        if x is None:
            self.x = []
        self.y = y
        if y is None:
            self.y = []
        self.percentage = percentage
        self.train_percentage = self.percentage_limiter(percentage)
        self.train_indices = None
        self.train_pool = None
        self.test_indices = None
        self.test_pool = None
        self.load_data(self.x, self.y)

    class Order(Enum):
        """Enum to define order data presented to network."""
        RANDOM = "random"
        SEQUENTIAL = "sequential"

    class Set(Enum):
        """Enum to define whether we are requesting test or training data."""
        TRAIN = "train"
        TEST = "test"

    @staticmethod
    def percentage_limiter(percentage: int):
        """Returns formatted value for percentage."""
        if percentage < 0:
            return 0
        elif percentage > 100:
            return 100
        return percentage

    def load_data(self, x, y):
        """Loads data for use."""
        if len(x) != len(y):
            raise DataMismatchError
        self.x = x
        self.y = y
        self.split_set()

    def split_set(self, new_train_percentage=None):
        """Takes incoming data and divides into training and test sets."""
        if new_train_percentage:
            self.train_percentage = self.percentage_limiter(new_train_percentage)

        size_of_training_set = int(len(self.x) * (self.train_percentage * .01))
        all_indices = list(range(len(self.x)))
        random.shuffle(all_indices)

        self.train_indices = all_indices[:size_of_training_set]
        self.test_indices = all_indices[size_of_training_set:]
        self.prime_data()

    def prime_data(self, my_set=None, order=None):
        """Prepares data pools."""
        if order is None:
            order = NNData.Order.SEQUENTIAL

        test_items = self.test_indices.copy()
        train_items = self.train_indices.copy()

        if order == NNData.Order.RANDOM:
            random.shuffle(test_items)
            random.shuffle(train_items)

        if not my_set or my_set == NNData.Set.TEST:
            self.test_pool = deque(test_items)
        if not my_set or my_set == NNData.Set.TRAIN:
            self.train_pool = deque(train_items)

    def empty_pool(self, my_set=None):
        """Checks if the data pool is empty."""
        if my_set is None:
            my_set = NNData.Set.TRAIN
        if my_set == NNData.Set.TRAIN:
            return len(self.train_pool) == 0
        return len(self.test_pool) == 0

    def get_number_samples(self, my_set=None):
        """Return length of sample data."""
        if my_set is None:
            return len(self.x)
        if my_set == NNData.Set.TEST:
            return len(self.test_indices)
        return len(self.train_indices)

    def get_one_item(self, my_set=None):
        """Return one item from the pool."""
        if my_set is None:
            my_set = NNData.Set.TRAIN
        if my_set == NNData.Set.TRAIN:
            pool = self.train_pool
        else:
            pool = self.test_pool
        if len(pool) == 0:
            return None
        index = pool.popleft()
        return [self.x[index], self.y[index]]
