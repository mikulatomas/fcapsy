from fcapy import Lattice, Context, Concept
from bitsets import bitset

import pytest
import xmltodict
import os


def cex_to_list(filename):
    with open(filename) as cex_file:
        content = xmltodict.parse(cex_file.read())

        cex_conceptual_system = content['ConceptualSystem']

        if cex_conceptual_system.get('Contexts'):
            cex_context = cex_conceptual_system['Contexts']['Context']

            context = extract_context(cex_context)

            if cex_conceptual_system.get('Lattices'):
                cex_lattice = cex_conceptual_system['Lattices']['Lattice']
                cex_concepts = cex_lattice['LineDiagram']['ConceptFigures']['LineDiagramFigure']

                concepts = extract_concepts(
                    cex_concepts, len(context['attributes']))

        return {
            'context': context,
            'concepts': concepts
        }


def extract_concepts(cex_concepts, n_of_attributes):
    concepts = []

    for concept in cex_concepts:
        intent = [False] * n_of_attributes

        if concept['Intent']:
            attrs = concept['Intent']['HasAttribute']

            if type(attrs) is list:
                for attr in attrs:
                    intent[int(attr['@AttributeIdentifier'])] = True
            else:
                intent[int(attrs['@AttributeIdentifier'])] = True

        concepts.append(intent)

    return concepts


def extract_context(cex_context):
    cex_attributes = cex_context['Attributes']['Attribute']
    cex_objects = cex_context['Objects']['Object']

    attributes = [attr['Name'] for attr in cex_attributes]
    objects = []
    table = []

    for obj in cex_objects:
        objects.append(obj['Name'])

        row = [False] * len(attributes)
        if obj['Intent'] is None:
            table.append(row)
            continue

        for intents in obj['Intent'].values():
            if type(intents) is list:
                for intent in intents:
                    row[int(intent['@AttributeIdentifier'])] = True
            else:
                row[int(intents['@AttributeIdentifier'])] = True

        table.append(row)

    return {
        'objects': tuple(objects),
        'attributes': tuple(attributes),
        'table': table
    }


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'lattices',
)


def load_all_lattices():
    paths = []

    directory = os.fsencode(FIXTURE_DIR)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".cex"):
            paths.append(os.path.join(FIXTURE_DIR, filename))

    return paths


ALL_LATTICES = pytest.mark.datafiles(*load_all_lattices())


# def create_context_from_list(context):
#     pass
# return [bitarray(row) for row in context]


@ALL_LATTICES
def test_lattice(datafiles):
    for lattice in datafiles.listdir():
        lattice_dict = cex_to_list(lattice)

        Objects = bitset('Objects', lattice_dict['context']['objects'])
        Attributes = bitset(
            'Attributes', lattice_dict['context']['attributes'])

        print(Objects.supremum.members())
        print(Attributes.supremum.members())

        context = Context(
            lattice_dict['context']['table'],
            Objects,
            Attributes)

        expected_concepts = []

        for intent in lattice_dict['concepts']:
            intent = Attributes.frombools(intent)
            extent = context.down(intent)
            expected_concepts.append(Concept(extent, intent))

        result = Lattice(context)

        assert len(expected_concepts) == len(result.get_concepts())
        assert set(expected_concepts) == set(result.get_concepts())


def test_lattice_creation():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    lattice = Lattice(context)

    assert len(lattice.get_concepts()) == 2
