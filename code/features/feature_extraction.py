import pickle

from ..base import StaticGraph, Network
from .static_features import compute_static_features
from .pairs_generator import get_train_set
from .temporal_features import compute_temporal_features


def load_graph(path, time_quantile: float = .8) -> StaticGraph:
    network = Network(path)
    return StaticGraph.from_time_slice(network, time_quantile)

def compute_features(graph):
    train_set = get_train_set(graph)
    static = compute_static_features(graph, train_set)
    temporal = compute_temporal_features(graph, train_set, .2)
    return {
        "edges_labels": train_set,
        "static": static,
        "second_a": temporal
    }

def save(features_dict, path):
    with open(path, "wb") as f:
        pickle.dump(features_dict, f)

def load(path):
    with open(path, "rb") as f:
        return pickle.load(f)
