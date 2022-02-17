import pytest
from playground import choose_lineage as cl


def test_cl_animal_person():
    temp = cl(hypo=['animal', 'object', 'plant'])
    assert temp == 'animal'

    temp = cl(hypo=['plant', 'object', 'person'])
    assert temp == 'person'

    temp = cl(hypo=['food', 'animal', 'person', 'plant'])
    assert temp == 'animal'


def test_cl_plant_food():
    temp = cl(hypo=['artifact', 'color', 'plant'])
    assert temp == 'plant'

    temp = cl(hypo=['concept', 'shape', 'food'])
    assert temp == 'food'

    temp = cl(hypo=['animal', 'food', 'plant', 'artifact', 'object'])
    assert temp == 'food'
