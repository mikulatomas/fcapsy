from itertools import combinations

from fcapy.decorators import metadata
from fcapy import Concept, Context


@metadata(name='RiceSiffConcepts', short_name='RSConcepts')
def concept_subset(context: Context, similarity_measure) -> list:
    """
    Experimental implementation of
    Rice, Michael D., and Michael Siff. "Clusters, concepts, and pseudometrics."
    Electronic Notes in Theoretical Computer Science 40 (2001): 323-346.
    """

    init_intent = context.Attributes.supremum
    init_extent = context.down(init_intent)

    init_concept = Concept(init_extent, init_intent)

    atoms = context.Objects.supremum.atoms()

    # init worklist with all atoms
    worklist = {Concept.from_intent(
        context.up(extent), context) for extent in atoms}

    # init resulting concepts with init_concept and worklist
    concepts = set(worklist)
    concepts.add(init_concept)

    while len(worklist) > 1:
        # create all possible pairs of different concepts from worklist
        concept_combinations = tuple(combinations(worklist, 2))

        # calculate all distances
        distances = [1 - similarity_measure(
            concepts[0].intent, concepts[1].intent) for concepts in concept_combinations]

        # select minimal distance from all distances
        min_distance = min(distances)

        # get all possible pairs of concepts with minimal distance
        concept_pairs_min_distance = {concept_tuple for concept_tuple, distance in zip(
            concept_combinations, distances) if distance == min_distance}

        # flatten pairs and transform them to set
        concepts_from_pairs = {
            concept for concept_pair in concept_pairs_min_distance for concept in concept_pair}

        # calculate new concepts and add them to worklist and result concepts
        for concept_tuple in concept_pairs_min_distance:
            extent = concept_tuple[0].extent | concept_tuple[1].extent
            new_intent = context.up(extent)
            new_extent = context.down(new_intent)
            new_concept = Concept(new_extent, new_intent)

            worklist.add(new_concept)
            concepts.add(new_concept)

        # remove already processed concepts
        worklist = worklist.difference(concepts_from_pairs)

    return concepts
