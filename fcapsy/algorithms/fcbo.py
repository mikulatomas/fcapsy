from collections import deque

from fcapsy import Concept, Context
from fcapsy.decorators import metadata


@metadata(name='FastCloseByOne', short_name='FCbO')
def fcbo(context: Context) -> list:
    """Calculates all concept of given concept.

    Outrata, Jan, and Vilem Vychodil. "Fast algorithm for computing fixpoints of Galois 
    connections induced by object-attribute relational data."
    Information Sciences 185.1 (2012): 114-127
    """
    Attributes = context.Attributes
    Objects = context.Objects

    attribute_count = len(Attributes.supremum)
    concepts = []

    def fast_generate_from(concept: Concept, attribute: int, attribute_sets: list):
        concepts.append(concept)

        if concept.intent.all() or attribute >= attribute_count:
            return

        queue = deque()
        set_my = attribute_sets.copy()
        intent_int = int(concept.intent)

        for j in range(attribute, attribute_count):
            tmp = 1 << j  # fast 2**j

            if intent_int & tmp:
                continue

            yj = tmp - 1

            x = attribute_sets[j]
            x &= yj

            y = intent_int
            y &= yj

            if x & y == x:
                c = context.columns[j]
                c &= concept.extent

                d = int(context.up(c))

                k = intent_int
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

    initial_concept = Concept.from_extent(Objects.supremum, context)

    attribute_sets = [0] * attribute_count

    fast_generate_from(initial_concept, 0, attribute_sets)

    return concepts
