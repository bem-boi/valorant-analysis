from __future__ import annotations
from typing import Any


class _WeightedVertex:
    item: Any
    kind: str
    neighbours: dict[_WeightedVertex, float]

    def __init__(self, item: Any, neighbours : dict[_WeightedVertex, float], kind : str) -> None:
        """Initialize a new vertex with the given item and kind and neighbours.

        Preconditions:
            - kind in {'map', 'agent'}
        """
        self.item = item
        self.neighbours = neighbours
        self.kind = kind

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class WeightedGraph:
    """A weighted graph.

    Representation Invariants:
    - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices: A collection of the vertices contained in this graph.
    #                  Maps item to _Vertex instance.
    _vertices: dict[Any, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        self._vertices[item] = _WeightedVertex(item, {}, kind)

    def add_edge(self, item1: Any, item2: Any, weight: float) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            # We didn't find an existing vertex for both items.
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.kind)

            for u in v.neighbours.keys():
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.kind)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item, weight=v.neighbours[u])

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


def load_weighted_graph(agent_pick_rates: str, teams_picked_agent: str) -> WeightedGraph:
    """
    The weight of the edge (for an agent-map edge) is calculated by the following formula:
        10 * ((Total Wins By Map) / (Total Maps Played) + Pick Rate)

    This acts as a measure for how good an agent is for a particular map

    """


def combine_and_clean_agents_pick_files(files: list[str]) -> str:
    """
    Create a file and return its path that is of the following format:
        Map,Agent,Pick Rate

    Only select rows where Map in {'Ascent', 'Bind', 'Haven', 'Icebox', 'Split', Breeze'}
    Get rows from every file referred to in files

    Precondition:
        - each item in files is a path to a CSV file
        - each CSV file being referred to has this same format:
            Tournament,Stage,Match Type,Map,Agent,Pick Rate
    """


def combine_and_clean_teams_picked_agents_files(files: list[str]) -> str:
    """
    Create a file and return its path that is of the following format:
        Map,Agent Picked,Total Wins By Map,Total Maps Played

    Only select rows where Map in {'Ascent', 'Bind', 'Haven', 'Icebox', 'Split', Breeze'}
    Get rows from every file referred to in files

    Precondition:
        - each item in files is a path to a CSV file
        - each CSV file being referred to has this same format:
            Tournament,Stage,Match Type,Map,Team,Agent Picked,Total Wins By Map,Total Loss By Map,Total Maps Played
    """
