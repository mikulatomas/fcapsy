import pytest
from bitsets import bitset
from fcapy.psychology.typicality import typicality_avg
from fcapy.similarity.objects import jaccard, smc, rosch


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_typicality_avg_1(similarity_function):
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([0, 1, 2, 3]),
    ]

    similarities = (similarity_function(objects[0], objects[0]),)

    expected = sum(similarities) / len(objects)

    assert typicality_avg(objects[0], objects,
                          similarity_function) == expected


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_typicality_avg_2(similarity_function):
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([0]),
        Attributes.frommembers([1]),
        Attributes.frommembers([2]),
        Attributes.frommembers([3]),
    ]

    similarities = (similarity_function(objects[0], objects[0]),
                    similarity_function(objects[0], objects[1]),
                    similarity_function(objects[0], objects[2]),
                    similarity_function(objects[0], objects[3]))

    expected = sum(similarities) / len(objects)

    assert typicality_avg(objects[0], objects,
                          similarity_function) == expected


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_typicality_avg_3(similarity_function):
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([0, 1, 2, 3]),
        Attributes.frommembers([0, 2]),
        Attributes.frommembers([3])
    ]

    similarities = (similarity_function(objects[0], objects[0]),
                    similarity_function(objects[0], objects[1]),
                    similarity_function(objects[0], objects[2]))

    expected = sum(similarities) / len(objects)

    assert typicality_avg(objects[0], objects,
                          similarity_function) == expected


@pytest.mark.parametrize("similarity_function", [smc, rosch])
def test_typicality_avg_4(similarity_function):
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([]),
        Attributes.frommembers([0, 1, 2, 3]),
    ]

    similarities = (similarity_function(objects[0], objects[0]),
                    similarity_function(objects[0], objects[1]))

    expected = sum(similarities) / len(objects)

    assert typicality_avg(objects[0], objects,
                          similarity_function) == expected
