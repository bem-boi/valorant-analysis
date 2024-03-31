from __future__ import annotations
from typing import Any, Union
import csv
import networkx as nx
from plotly.graph_objs import Figure


class _WeightedVertex:
    item: Any
    kind: str
    neighbours: dict[_WeightedVertex, float]
    role: str

    def __init__(self, item: Any, neighbours: dict[_WeightedVertex, float], kind: str, role: str = None) -> None:
        """Initialize a new vertex with the given item and kind and neighbours.

        Preconditions:
            - kind in {'map', 'agent'}
        """
        self.item = item
        self.neighbours = neighbours
        self.kind = kind
        self.role = role

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

    def add_vertex(self, item: Any, kind: str, role: str = None) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        self._vertices[item] = _WeightedVertex(item, {}, kind, role)

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
        if not self.adjacent(item1, item2):
            return 0
        else:
            v1 = self._vertices[item1]
            return [v1.neighbours[v2] for v2 in v1.neighbours if v2.item == item2][0]

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

    def check_exists(self, item: Any) -> bool:
        """

        :return:
        """
        return item in self._vertices

    def get_vertex(self, item: Any) -> _WeightedVertex:
        """

        :param item:
        :return:
        """
        return self._vertices[item]

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


def load_agent_role_data(agent_role: str) -> dict[str: str]:
    """

    :param agent_role: file where the data of agents and their roles are kept
    :return: returns a dictionary of the agents and their roles
    """
    agent = {}
    with open(agent_role, 'r') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader:
            agent[row[0].lower()] = row[1].lower()
    return agent


def load_map_agent_data(agent_pick_rates: str, teams_picked_agent: str, agent_roles: dict) -> dict[str, dict[str, list]]:
    """
    Return a dictionary where the keys are all the maps in the csv files (referred to by the arguments)
    and where the values are dictionaries whose keys are all the agents in the csv files
    and the values are lists storing sum of pick rates, count of pick rates, total wins so far and total played so far.

    In other words, the dictionary will be in the format {map_name: agent_ref}
    where agent_ref is in the format
    {agent_name: [sum_pick_rate, count_pick_rate, total_wins, total_played, role]}

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
                map_ref[row[0]] = {row[1]: [float(row[2]), 1, 0, 0, agent_roles[row[1]]]}  # define new map in map_ref & new agent_ref for it
            elif row[1] not in map_ref[row[0]]:  # if the agent is not in the agent_ref of this map key
                map_ref[row[0]][row[1]] = [float(row[2]), 1, 0, 0, agent_roles[row[1]]]  # create a new agent_ref for it
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


def generate_weighted_graph(map_ref: dict[str, dict[str, list]], role: str = None, cu_map: str = 'all') -> WeightedGraph:
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
        - role in agent_role.values()
        - cu_map in {'ascent', 'pearl', 'split', 'lotus', 'icebox', 'fracture', 'bind', 'haven', 'all'}
    """
    g = WeightedGraph()
    if cu_map == 'all':
        for map_name in map_ref:
            g.add_vertex(map_name, 'map')
            for agent_name in map_ref[map_name]:
                if (role is None) or (map_ref[map_name][agent_name][4] == role):
                    if not g.check_exists(agent_name):
                        g.add_vertex(agent_name, 'agent', map_ref[map_name][agent_name][4])
                    if map_ref[map_name][agent_name][3] == 0 or map_ref[map_name][agent_name][1] == 0:
                        weight = 0
                    else:
                        weight = (10 * (map_ref[map_name][agent_name][2] / map_ref[map_name][agent_name][3]) +
                                  5 * (map_ref[map_name][agent_name][0] / map_ref[map_name][agent_name][1]))
                    g.add_edge(map_name, agent_name, round(weight, 2))
    else:
        g.add_vertex(cu_map, 'map')
        for agent_name in map_ref[cu_map]:
            if (role is None) or (map_ref[cu_map][agent_name][4] == role):
                if not g.check_exists(agent_name):
                    g.add_vertex(agent_name, 'agent', map_ref[cu_map][agent_name][4])
                if map_ref[cu_map][agent_name][3] == 0 or map_ref[cu_map][agent_name][1] == 0:
                    weight = 0
                else:
                    weight = (10 * (map_ref[cu_map][agent_name][2] / map_ref[cu_map][agent_name][3]) +
                              5 * (map_ref[cu_map][agent_name][0] / map_ref[cu_map][agent_name][1]))
                g.add_edge(cu_map, agent_name, round(weight, 2))
    return g


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
                    writer.writerow([row[3].lower(), row[4], int(row[5][:-1]) / 100])
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
                writer.writerow([row[3].lower(), row[5], row[6], row[8]])
    return 'cleaned_teams_picked_agents.csv'


def best_agent_for_map(graph: WeightedGraph, map_played: str, teammate: list, role: str = '') -> dict[str: float]:
    """

    :param role: role the player wants to play
    :param teammate: what agents are your teammates playing
    :param graph: Weighted graph where all the data is being held
    :param map_played: the current map being played (input from user)
    :return: returns a dictionary of agents and the score from 0-15 of how good the agent is for that map
    """

    agent_and_score = {}
    for agent in graph.get_neighbours(map_played):
        if agent not in teammate and (not role or graph.get_vertex(agent).role == role):
            agent_and_score[agent] = graph.get_weight(agent, map_played)

    sorted_agent_and_score = dict(sorted(agent_and_score.items(), key=lambda item: item[1], reverse=True))
    return sorted_agent_and_score


def visualize_graph(agents_roles: dict, map_ref: dict, role: str = '') -> None:
    """
    Visualize a graph of agents of type role only and maps.
    If role is an empty string, then visualize graphs for all roles
    :param agents_roles:
    :param map_ref:
    :param role:
    :return:
    """
    from visualization import visualize_weighted_graph
    if role:
        g = generate_weighted_graph(map_ref, role)
        visualize_weighted_graph(g)
    else:
        for role in set(agents_roles.values()):
            g = generate_weighted_graph(map_ref, role)
            visualize_weighted_graph(g)


def return_graph(map_ref: dict, role: str, cur_map: str) -> Figure:
    """

    :param cur_map: 
    :param agents_roles:
    :param map_ref:
    :param role:
    :return:
    """
    from visualization import return_weighted_graph
    if role == 'all' and cur_map == 'all':
        g = generate_weighted_graph(map_ref)
    elif role == 'all' and cur_map != 'all':
        g = generate_weighted_graph(map_ref, cu_map=cur_map)
    else:
        g = generate_weighted_graph(map_ref, role, cur_map)
    return return_weighted_graph(g)


# ---MAIN---
if __name__ == '__main__':
    cleaned_agf_file = clean_agents_pick_file('graph_data/agents_pick_rates2023.csv')
    cleaned_tpa_file = clean_teams_picked_agents_file('graph_data/teams_picked_agents2023.csv')
    agent_role_data = load_agent_role_data('graph_data/agent_roles.csv')

    map_agent_data = load_map_agent_data(cleaned_agf_file, cleaned_tpa_file, agent_role_data)
    map_agent_graph = generate_weighted_graph(map_agent_data)

    # current_map = input("What map are you playing?").lower()
    # favored_role = input("What role do you want to play? Press ENTER if you have no preference").lower()  # pressing
    # # enter would make it '' type
    # teammate_ask = input("Do you want the recommendation to be based on what agents your teammates are playing? Type "
    #                      "'NO' if you don't want it to be considered. Otherwise type 'YES'. ").upper()
    # teammate_data = []
    # if teammate_ask == 'YES':
    #     for i in range(4):
    #         teammate_data.append(input(str(i + 1) + ": What agent is this teammate playing?").lower())
    #
    # agents_to_play = best_agent_for_map(map_agent_graph, current_map, teammate_data, favored_role)  # list of agents
    # # that the user should play on that map
    # print(agents_to_play)

    # visualize_graph(agent_role_data, map_agent_data, '')
