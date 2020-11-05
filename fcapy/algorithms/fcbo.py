from fcapy import Concept
from collections import deque
from copy import copy
from fcapy.decorators import metadata


@metadata(name='FastCloseByOne', short_name='FCbO')
def fcbo(context: Context) -> list:
    """Calculates all concept of given concept"""

    initial_concept = Concept(context._Objects.supremum,
                              context.up(context._Objects.supremum))

    Attributes = context._Attributes
    Objects = context._Objects

    attribute_count = context._Attributes.supremum.count()
    concepts = []
    attribute_sets = [0] * attribute_count

    def fast_generate_from(concept: Concept, attribute: int, attribute_sets: list):
        concepts.append(concept)

        if concept.intent.all() or attribute >= attribute_count:
            return

        queue = deque()
        set_my = copy(attribute_sets)
        intent_int = int(concept.intent)

        for j in range(attribute, attribute_count):
            tmp = 2 ** j
            yj = tmp - 1
            b = intent_int

            x = attribute_sets[j]
            x &= yj

            y = b
            y &= yj

            # faster than other way 'not b & tmp and x & y == x'
            if x & y == x and not b & tmp:
                c = context.columns[j]
                c &= concept.extent

                d = int(context.up(c))

                k = b
                k &= yj

                l = d
                l &= yj

                if k == l:
                    queue.append((Concept(Objects.fromint(c),
                                          Attributes.fromint(d)), j + 1))
                else:
                    set_my[j] = d

        while queue:
            concept, j = queue.popleft()
            fast_generate_from(concept,
                               j,
                               set_my)

    fast_generate_from(initial_concept, 0, attribute_sets)

    return concepts
