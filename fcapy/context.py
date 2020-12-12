from itertools import compress
from bitsets.bases import BitSet
from typing import Type, Tuple, Iterator
from bitsets import bitset
import csv
import random


class Context:
    def __init__(self, matrix: list, objects_labels: list, attributes_labels: list):
        self._Objects = bitset('Objects', objects_labels)
        self._Attributes = bitset('Attributes', attributes_labels)

        self.rows = tuple(map(self._Attributes.frombools, matrix))
        self.columns = tuple(map(self._Objects.frombools, zip(*matrix)))

    def __repr__(self):
        return f"Context({len(self.rows)}x{len(self.columns)})"

    @classmethod
    def from_random(cls, number_of_objects, number_of_attributes):
        matrix = [random.choices([0, 1], k=number_of_attributes)
                  for i in range(number_of_objects)]

        return cls(matrix, tuple(range(number_of_objects)), tuple(range(number_of_attributes)))

    @classmethod
    def from_pandas(cls, dataframe):
        return cls(dataframe.values, tuple(dataframe.index), tuple(dataframe.columns))

    @classmethod
    def from_csv(cls, filename: str, objects_labels: list = [], attribute_labels: list = [], delimiter: str = ','):
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file, delimiter=delimiter)

            bools = []
            labels = []

            for idx, row in enumerate(csv_reader):
                if idx == 0 and not attribute_labels:
                    attribute_labels = tuple(row[1:])
                else:
                    if not objects_labels:
                        labels.append(row.pop(0))

                    bools.append(tuple(map(int, row)))

            if not objects_labels:
                objects_labels = labels

        return cls(bools, tuple(objects_labels), tuple(attribute_labels))

    @classmethod
    def from_fimi(cls, filename: str, objects_labels: list = None, attribute_labels: list = None):
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

        return cls(bools, objects_labels, attribute_labels)

    def to_bools(self) -> Iterator[tuple]:
        return map(self._Attributes.bools, self.rows)

    @property
    def shape(self) -> Tuple[int, int]:
        return (len(self.rows), len(self.columns))

    def filter(self, by: Type[BitSet]) -> Iterator[Type[BitSet]]:
        if isinstance(by, self._Objects):
            filter_target = self.rows
        elif isinstance(by, self._Attributes):
            filter_target = self.columns
        else:
            raise ValueError

        return compress(filter_target, by.bools())

    def __arrow_operator(self, input_set: Type[BitSet], data: tuple, ResultClass) -> Type[BitSet]:
        """Experimental implementation based on:
        https://stackoverflow.com/q/63917579/3456664"""

        result = ResultClass.supremum
        i = 0

        while i < len(data):
            if input_set:
                trailing_zeros = (input_set ^ (input_set - 1)).bit_length() - 1
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
        return self.__arrow_operator(objects, self.rows, self._Attributes)

    def down(self, attributes: Type[BitSet]) -> Type[BitSet]:
        return self.__arrow_operator(attributes, self.columns, self._Objects)
