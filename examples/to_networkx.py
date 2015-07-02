"""
Using the edge list in Python (using the NetworkX package).
"""

import networkx as nx

DATA_PATH = '../data/edgelist.csv'


def edgelist_to_networkx(data_path=DATA_PATH):
    """
    Convert an edgelist file into a NetworkX representation of the graph. Transmitters, receptors and their respective
    sources are stored as dictionaries in the node attributes. Each edge's transmitter, receptor, and minimum distance
    are stored as edge attributes.

    :param data_path: The path to the data file (default '../data/edgelist.csv')
    :type data_path: str
    :return: A NetworkX representation of the graph including all edge and node attributes.
    :rtype: nx.MultiDiGraph
    """
    graph = nx.MultiDiGraph()
    with open(data_path) as f:
        next(f)  # skip the header row
        for line in f:
            source, target, transmitter, receptor, minimum_distance, source_doi, target_doi = \
                (field.strip() for field in line.split(','))

            for node in (source, target):
                if node not in graph.node:
                    graph.add_node(node, transmitters=dict(), receptors=dict())

            graph.node[source]['transmitters'][transmitter] = source_doi
            graph.node[source]['receptors'][receptor] = target_doi

            graph.add_edge(source, target, key=receptor, minimum_distance=float(minimum_distance),
                           transmitter=transmitter, receptor=receptor)

    return graph

if __name__ == '__main__':
    graph = edgelist_to_networkx()