from __future__ import annotations
from typing import Any
import csv
import networkx as nx


class _WeightedVertex:
    item: Any
    kind: str
    neighbours: dict[_WeightedVertex, float]

    def __init__(self, item: Any, neighbours: dict[_WeightedVertex, float], kind: str) -> None:
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


def load_map_agent_data(agent_pick_rates: str, teams_picked_agent: str) -> dict[str, dict[str, list]]:
    """
    Return a dictionary where the keys are all the maps in the csv files (referred to by the arguments)
    and where the values are dictionaries whose keys are all the agents in the csv files
    and the values are lists storing sum of pick rates, count of pick rates, total wins so far and total played so far.

    In other words, the dictionary will be in the format {map_name: agent_ref}
    where agent_ref is in the format {agent_name: [sum_pick_rate, count_pick_rate, total_wins, total_played]}

    Preconditions:
        - Each row in the csv referred to by agent_pick_rates is in the format:
            [Map,Agent,Pick Rate]
        - Each row in the csv referred to by teams_picked_agent is in the format:
            [Map,Agent Picked,Total Wins By Map,Total Maps Played]
    """
    map_ref = {}  # {map_name: agent_ref} and agent_ref in format
    # {agent_name: [sum_pick_rate_so_far, count_pick_rate_so_far, total_wins_so_far, total_played_so_far]}
    with open(agent_pick_rates, 'r') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader:
            if row[0] not in map_ref:  # if the map is not in map_ref
                map_ref[row[0]] = {row[1]: [float(row[2]), 1, 0, 0]}  # define new map in map_ref & new agent_ref for it
            elif row[1] not in map_ref[row[0]]:  # if the agent is not in the agent_ref of this map key
                map_ref[row[0]][row[1]] = [float(row[2]), 1, 0, 0]  # create a new agent_ref for it
            else:  # the map is already in map_ref and the agent is already in its agent_ref
                map_ref[row[0]][row[1]][0] += float(row[2])  # update sum_pick_rate_so_far
                map_ref[row[0]][row[1]][1] += 1  # update count_pick_rate_so_far
    with open(teams_picked_agent, 'r') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader:
            map_ref[row[0]][row[1]][2] += int(row[2])  # update total_wins_so_far
            map_ref[row[0]][row[1]][3] += int(row[3])  # update total_played_so_far
    return map_ref


def generate_weighted_graph(map_ref: dict[str, dict[str, list]]) -> WeightedGraph:
    """
    Return a weighted graph where:

    - The vertices are the different maps and the agents in the csv files provided

    - The weight of the edges (for agent-map edges) is calculated by the following formula:
        IF (Total Maps Played = 0 or Number of Times Picked = 0),
            THEN 0
        ELSE
            10 * ((Total Wins By Map) / (Total Maps Played)) +  5 * (Sum Pick Rate Percentages / Number of Times Picked)

      This acts as a measure for how good an agent is for a particular map (weight will be between 0 and 15)

    Precondition:
        - map_ref is in the format {map_name: agent_ref}
        where agent_ref is in the format {agent_name: [sum_pick_rate, total_wins, total_played]}
    """
    g = WeightedGraph()
    for map_name in map_ref:
        g.add_vertex(map_name, 'map')
        for agent_name in map_ref[map_name]:
            g.add_vertex(agent_name, 'agent')
            if map_ref[map_name][agent_name][3] == 0 or map_ref[map_name][agent_name][1] == 0:
                weight = 0
            else:
                weight = (10 * (map_ref[map_name][agent_name][2] / map_ref[map_name][agent_name][3]) +
                          5 * (map_ref[map_name][agent_name][0] / map_ref[map_name][agent_name][1]))
            g.add_edge(map_name, agent_name, weight)
    return WeightedGraph()


def clean_agents_pick_file(file: str) -> str:
    """
    Create a file and return its path that is of the following format:
        Map,Agent,Pick Rate
    where pick rate is written as a decimal between 0 and 1 (e.g. 0.16 to represent 16%)

    Do not select rows where Map = 'All Maps'

    Precondition:
        - file is a path to a CSV file
        - the CSV file being referred to has the following format:
            Tournament,Stage,Match Type,Map,Agent,Pick Rate
    """
    with open('cleaned_agents_pick_rates.csv', 'w', newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(['Map', 'Agent', 'Pick Rate'])
        with open(file, 'r') as read_file:
            next(read_file)
            reader = csv.reader(read_file)
            for row in reader:
                if row[3] != 'All Maps':
                    writer.writerow([row[3], row[4], int(row[5][:-1]) / 100])
    return 'cleaned_agents_pick_rates.csv'


def clean_teams_picked_agents_file(file: str) -> str:
    """
    Create a file and return its path that is of the following format:
        Map,Agent Picked,Total Wins By Map,Total Maps Played

    Precondition:
        - file is a path to a CSV file
        - the CSV file being referred to has the following format:
            Tournament,Stage,Match Type,Map,Team,Agent Picked,Total Wins By Map,Total Loss By Map,Total Maps Played
    """
    with open('cleaned_teams_picked_agents.csv', 'w', newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(['Map', 'Agent Picked', 'Total Wins By Map', 'Total Maps Played'])
        with open(file, 'r') as read_file:
            next(read_file)
            reader = csv.reader(read_file)
            for row in reader:
                writer.writerow([row[3], row[5], row[6], row[8]])
    return 'cleaned_teams_picked_agents.csv'


# ---MAIN---

cleaned_agf_file = clean_agents_pick_file('graph_data/agents_pick_rates2023.csv')
cleaned_tpa_file = clean_teams_picked_agents_file('graph_data/teams_picked_agents2023.csv')

map_agent_data = load_map_agent_data(cleaned_agf_file, cleaned_tpa_file)
map_agent_graph = generate_weighted_graph(map_agent_data)

