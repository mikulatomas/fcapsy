import csv
from bitsets import bitset
from scipy.sparse import random


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
    with open(filename) as file:
        items = []
        for line in file:
            items.append(line.replace('\n', ''))

        return items


def calculate_density(bools):
    width = len(bools[0])
    height = len(bools)

    n_of_cells = width * height

    n_of_ones = 0

    for row in bools:
        n_of_ones += row.count(True)

    return (n_of_ones / n_of_cells) * 100


def generate_random_boolean_dataset(m, n, density):
    bools = random(m, n, density, dtype=bool).A
    Objects = bitset('Objects', tuple(range(m)))
    Attributes = bitset('Attributes', tuple(range(n)))

    return Objects, Attributes, bools
