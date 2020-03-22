import csv
from bitsets import bitset
from fcapy import Context


def context_from_dataframe(df):
    Objects = bitset('Objects', tuple(df.index))
    Attributes = bitset('Attributes', tuple(df.columns))

    return Context(matrix=df.values, Objects=Objects, Attributes=Attributes)


def load_sparse_csv(filename, filename_attributes, delimiter=','):
    """
    Loads .csv in format from dataset and universum:
    object1, attribute1, attribute10, attribute 20
    object2, attribute2, attribute30
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


def __load_items_from_file(filename):
    return [line.rstrip('\n') for line in open(filename)]
