from itertools import compress
from bitsets.bases import BitSet
from typing import Type
from bitsets import bitset
import csv


class Context:
    def __init__(self, matrix: list, objects_labels: list, attributes_labels: list):
        self._Objects = bitset('Objects', objects_labels)
        self._Attributes = bitset('Attributes', attributes_labels)

        self.rows = tuple(map(self._Attributes.frombools, matrix))
        self.columns = tuple(map(self._Objects.frombools, zip(*matrix)))

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

    def up(self, objects: Type[BitSet]) -> Type[BitSet]:
        return self.__arrow_operator(objects, self.rows, self._Attributes)

    def down(self, attributes: Type[BitSet]) -> Type[BitSet]:
        return self.__arrow_operator(attributes, self.columns, self._Objects)

    def get_bools(self) -> tuple:
        return tuple(map(self._Attributes.bools, self.rows))

    def filter_rows_by_extent(self, extent: Type[BitSet]) -> tuple:
        return tuple(compress(self.rows, extent.bools()))

    def filter_columns_by_intent(self, intent: Type[BitSet]) -> tuple:
        return tuple(compress(self.columns, intent.bools()))

    def __arrow_operator(self, input_set: Type[BitSet], data: tuple, ResultClass) -> Type[BitSet]:
        """Experimental implementation based on:
        https://stackoverflow.com/q/63917579/3456664"""

        result = ResultClass.supremum
        i = 0

        bit_lenght = int.bit_length

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
