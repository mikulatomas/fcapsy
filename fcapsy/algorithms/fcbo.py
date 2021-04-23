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

    def fast_generate_from(queue: deque):
        while queue:
            concept, attribute, attribute_sets = queue.popleft()

            yield concept

            if concept.intent.all() or attribute >= attribute_count:
                continue

            set_my = attribute_sets.copy()
            intent_int = int(concept.intent)

            for j in range(attribute, attribute_count):
                tmp = 1 << j  # fast 2**j

                if intent_int & tmp:
                    continue

                yj = tmp - 1

                x = attribute_sets[j] & yj

                if x & intent_int == x:
                    c = context.columns[j] & concept.extent
                    d = int(context.up(c))

                    if intent_int & yj == d & yj:
                        next_concept = Concept(Objects.fromint(c), Attributes.fromint(d))
                        queue.append((next_concept, j + 1, set_my))
                    else:
                        set_my[j] = d

    initial_concept = Concept.from_extent(Objects.supremum, context)

    attribute_sets = [0] * attribute_count

    queue = deque([(initial_concept, 0, attribute_sets)])
    concepts = fast_generate_from(queue)
    return list(concepts)
