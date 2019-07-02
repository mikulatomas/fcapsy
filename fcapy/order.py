from fcapy import Concept
from collections import deque

UPPER = 'upper'
LOWER = 'lower'


def calculate_upper_neighbors(context, concept):
    minimal = ~concept.extent

    for objects in context._Objects.atomic(minimal):
        new_intent = context.up(concept.extent | objects)
        new_extent = context.down(new_intent)

        if minimal & (new_extent & ~objects):
            minimal &= ~objects
        else:
            neighbor = Concept(
                context._Objects.fromint(new_extent),
                context._Attributes.fromint(new_intent))

            yield neighbor


def calculate_lattice(context):
    lattice = {}

    init_intent = context._Attributes.supremum
    init_extent = context._Objects.fromint(context.down(init_intent))

    init_concept = Concept(init_extent, init_intent)

    lattice[init_concept] = {UPPER: set(), LOWER: set()}

    queue = deque((init_concept, ))

    while queue:
        concept = queue.pop()

        for neighbor in calculate_upper_neighbors(context, concept):
            existing_neighbor = lattice.get(neighbor)

            if not existing_neighbor:
                lattice[neighbor] = {UPPER: set(), LOWER: set((concept, ))}
            else:
                existing_neighbor[LOWER].add(concept)

            lattice[concept][UPPER].add(neighbor)

            queue.append(neighbor)

    return lattice
