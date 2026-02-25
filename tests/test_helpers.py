import dataclasses

from utils.helpers import seq_to_routes


def test_seq_to_routes(sample_data):
    # setup
    seq = [2, 4, 5, 6, 3]

    routes = seq_to_routes(sample_data, seq)
    assert routes == [[2, 4], [5, 6], [3]]

    sample_data = dataclasses.replace(sample_data, capacity=1000)
    routes = seq_to_routes(sample_data, seq)
    assert routes == [seq]

    sample_data = dataclasses.replace(sample_data, capacity=0)
    routes = seq_to_routes(sample_data, seq)
    assert routes == []
