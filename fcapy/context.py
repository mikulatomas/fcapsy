from itertools import compress
from bitsets import bitset


class Context:
    def __init__(self, matrix, Objects, Attributes):
        self.rows = tuple(map(Attributes.frombools, matrix))
        self.columns = tuple(map(Objects.frombools, zip(*matrix)))

        self._Objects = Objects
        self._Attributes = Attributes

    @classmethod
    def from_fimi(cls, filename, objects_labels=None, attribute_labels=None):
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
            objects_labels = range(len(bools))

        if attribute_labels is None:
            attribute_labels = range(len(bools[0]))

        return cls(bools, bitset("Objects", objects_labels), bitset("Attributes", attribute_labels))

    def up(self, objects):
        return self.__arrow_operator(objects, self.rows, self._Attributes)

    def down(self, attributes):
        return self.__arrow_operator(attributes, self.columns, self._Objects)

    def get_bools(self):
        return tuple(map(self._Attributes.bools, self.rows))

    def filter_rows_by_extent(self, extent):
        return tuple(compress(self.rows, extent.bools()))

    def filter_columns_by_intent(self, intent):
        return tuple(compress(self.columns, intent.bools()))

    def __arrow_operator(self, input_set, data, ResultClass):
        """Experimental implementation based on:
        https://stackoverflow.com/q/63917579/3456664"""

        result = ResultClass.supremum
        i = 0

        while i < len(data):
            if input_set:
                trailing_zeros = (input_set ^ -input_set).bit_length() - 2
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
