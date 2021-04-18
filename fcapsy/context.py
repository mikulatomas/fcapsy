import csv
import random
from typing import Type, Tuple, Iterator
from itertools import compress

from bitsets.bases import BitSet
from bitsets import bitset


class Context:
    def __init__(self, matrix: list, objects_labels: list, attributes_labels: list, name: str = None):
        self.Objects = bitset('Objects', tuple(objects_labels))
        self.Attributes = bitset('Attributes', tuple(attributes_labels))

        self.rows = tuple(map(self.Attributes.frombools, matrix))
        self.columns = tuple(map(self.Objects.frombools, zip(*matrix)))
        self.name = name

    def __repr__(self):
        if self.name:
            return "Context({}, {}x{})".format(self.name, len(self.rows), len(self.columns))

        return "Context({}x{})".format(len(self.rows), len(self.columns))

    def __eq__(self, other):
        if isinstance(self, type(other)):
            return ((self.rows == other.rows) and
                    (self.columns == other.columns) and
                    (self.Objects.supremum.members() == other.Objects.supremum.members()) and
                    (self.Attributes.supremum.members() == other.Attributes.supremum.members()))

    @classmethod
    def from_random(cls, number_of_objects, number_of_attributes):
        matrix = [random.choices([0, 1], k=number_of_attributes)
                  for i in range(number_of_objects)]

        return cls(matrix, tuple(range(number_of_objects)), tuple(range(number_of_attributes)))

    @classmethod
    def from_pandas(cls, dataframe, name: str = None):
        return cls(dataframe.values, tuple(dataframe.index), tuple(dataframe.columns), name=name)

    @classmethod
    def from_fimi(cls, filename: str, objects_labels: list = None, attribute_labels: list = None, name: str = None):
        with open(filename, 'r') as file:
            max_attribute = 0
            rows = []

            for line in file:
                # remove '\n' from line
                line = line.strip()
                row_attributes = []

                for value in line.split():
                    attribute = int(value)
                    row_attributes.append(attribute)
                    max_attribute = max(attribute, max_attribute)

                rows.append(row_attributes)

            bools = [[True if i in row else False for i in range(max_attribute + 1)]
                     for row in rows]

        if objects_labels is None:
            objects_labels = tuple(map(str, range(len(bools))))

        if attribute_labels is None:
            attribute_labels = tuple(map(str, range(len(bools[0]))))

        return cls(bools, objects_labels, attribute_labels, name=name)

    def to_bools(self) -> Iterator[tuple]:
        return map(self.Attributes.bools, self.rows)

    @property
    def density(self) -> float:
        return sum([sum(row.bools()) for row in self.rows]) / \
            (self.shape[0] * self.shape[1])

    @property
    def shape(self) -> Tuple[int, int]:
        return (len(self.rows), len(self.columns))

    def filter(self, items: list = None, axis: int = 0) -> Iterator[Type[BitSet]]:
        if axis == 0:
            target = self.rows
            data_class = self.Objects
        elif axis == 1:
            target = self.columns
            data_class = self.Attributes
        else:
            ValueError("Axis should be 0 or 1.")

        return compress(target, data_class(items).bools())

    def __arrow_operator(self, input_set: Type[BitSet], data: tuple, ResultClass) -> Type[BitSet]:
        """Experimental implementation based on:
        https://stackoverflow.com/q/63917579/3456664"""

        result = ResultClass.supremum
        i = 0

        while i < len(data):
            if input_set:
                trailing_zeros = (input_set & -input_set).bit_length() - 1
                if trailing_zeros:
                    input_set >>= trailing_zeros
                    i += trailing_zeros
                else:
                    result &= data[i]
                    input_set >>= 1
                    i += 1
            else:
                break

        return ResultClass.fromint(result)

    def up(self, objects: Type[BitSet]) -> Type[BitSet]:
        return self.__arrow_operator(objects, self.rows, self.Attributes)

    def down(self, attributes: Type[BitSet]) -> Type[BitSet]:
        return self.__arrow_operator(attributes, self.columns, self.Objects)
