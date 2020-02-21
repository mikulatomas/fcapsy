import csv
from bitsets import bitset


def load_sparse_csv(filename, filename_attributes, delimiter=','):
    """
    Loads .csv in format from dataset and universum:
    object1, attribute1, attribute10, attribute 20
    object2, attribute2, attribute 30
    """

    attributes = __load_items_from_file(filename_attributes)
    attributes_hash = {attribute: index for index,
                       attribute in enumerate(attributes)}

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        bools = []
        objects = []

        for row in reader:
            bool_row = [0] * len(attributes)

            for attr in row[1:]:
                bool_row[attributes_hash[attr]] = 1

            bools.append(bool_row)
            objects.append(row[0])

        Objects = bitset('Objects', tuple(objects))
        Attributes = bitset('Attributes', tuple(attributes))

        return Objects, Attributes, bools


def load_csv(filename, filename_objects=None, filename_attributes=None, delimiter=','):
    if (filename_objects is None) and (filename_attributes is None):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
            rows = []
            objects = []

            for idx, row in enumerate(reader):
                if idx == 0:
                    attributes = row[1:]
                else:
                    rows.append(list(map(int, row[1:])))
                    objects.append(row[0])

            Objects = bitset('Objects', tuple(objects))
            Attributes = bitset('Attributes', tuple(attributes))
            bools = rows

            return Objects, Attributes, bools
    else:
        objects = __load_items_from_file(filename_objects)
        attributes = __load_items_from_file(filename_attributes)

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
            rows = []

            for idx, row in enumerate(reader):
                rows.append(list(map(int, row)))

            Objects = bitset('Objects', tuple(objects))
            Attributes = bitset('Attributes', tuple(attributes))
            bools = rows

            return Objects, Attributes, bools


def __load_items_from_file(filename):
    return [line.rstrip('\n') for line in open(filename)]


def calculate_density(bools):
    width = len(bools[0])
    height = len(bools)

    n_of_cells = width * height

    n_of_ones = 0

    for row in bools:
        n_of_ones += row.count(True)

    return (n_of_ones / n_of_cells) * 100
