"""
trees r slay
"""
from __future__ import annotations
from typing import Any, Optional, TextIO

from dash.html import Figure
from igraph import Graph
import plotly.graph_objects as go


class Tree:
    """A recursive tree graph_data structure.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            return 1 + sum(subtree.__len__() for subtree in self._subtrees)

    def __repr__(self) -> str:
        """Return a one-line string representation of this tree.

        >>> t = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> t
        Tree(2, [Tree(4, []), Tree(5, [])])
        """
        return f"Tree({self._root}, {self._subtrees})"

    def insert_sequence(self, items: list) -> None:
        """Insert the given items into this tree.

        The inserted items form a chain of descendants, where:
            - items[0] is a child of this tree's root
            - items[1] is a child of items[0]
            - items[2] is a child of items[1]
            - etc.

        Do nothing if items is empty.

        Preconditions:
            - not self.is_empty()

        >>> t = Tree(111, [])
        >>> t.insert_sequence([1, 2, 3])
        >>> print(t)
        111
          1
            2
              3
        >>> t.insert_sequence([1, 3, 5])
        >>> print(t)
        111
          1
            2
              3
            3
              5
        >>> t = Tree(10, [Tree(2, [Tree(3, [])])])
        >>> t.insert_sequence([2, 3, 4])
        >>> t
        Tree(10, [Tree(2, [Tree(3, [Tree(4, [])])])])

        >>> t = Tree(10, [Tree(2, [Tree(3, [])])])
        >>> t.insert_sequence([2, 3])
        >>> t
        Tree(10, [Tree(2, [Tree(3, [])])])

        >>> t = Tree(10, [Tree(2, [Tree(3, [])])])
        >>> t.insert_sequence([10, 2, 3])
        >>> print(t)
        10
          2
            3
          10
            2
              3
        """
        if items:
            if all(items[0] != subt._root for subt in self._subtrees):
                new_tree = Tree(items[0], [])
                new_tree._insert_helper(items[1:])
                self._subtrees.append(new_tree)
            else:
                for subtree in self._subtrees:
                    if items[0] == subtree._root:
                        subtree.insert_sequence(items[1:])
                        break

    def _insert_helper(self, items: list[int]) -> None:
        """
        Inserts a subtree sequence from a given list of items, where items is
        a sequence of elements [x_1, x_2,...,x_k] and they are inserted into the tree
        such that x_1 is a child of the tree’s root, x_2 is a child of x_1, x_3 is a
        child of x_2, etc.
        >>> t = Tree(10, [])
        >>> t._insert_helper([2, 3])
        >>> t
        Tree(10, [Tree(2, [Tree(3, [])])])
        """
        if items:
            self._subtrees.append(Tree(items[0], []))
            for subtree in self._subtrees:
                subtree._insert_helper(items[1:])

    def _best_side_helper(self) -> tuple[int, int]:
        return (self._subtrees[0]._root[0], self._subtrees[0]._root[1])

    def best_side_for_map(self, map_played: str) -> str:
        """
        Returns a string stating whether the user is more likely to win on the given map (map_player)
        as an Attacker or Defender based on the data from self.
        """
        attack = 0
        defend = 0
        for subtree1 in self._subtrees:
            for subtree2 in subtree1._subtrees:
                for subtree3 in subtree2._subtrees:
                    if subtree3._root.lower() == map_played:
                        for subtree4 in subtree3._subtrees:
                            attack, defend = subtree4._best_side_helper()
        if attack > defend:
            return "is Attacker sided"
        if attack < defend:
            return "is Defender sided"
        else:
            return "favours both sides"

    def _best_buy_helper(self, eco: int, semi_eco: int, semi_buy: int, full: int) -> None:
        for subtree in self._subtrees:
            if subtree._root[1] == 'Eco: 0-5k':
                eco += 1
            elif subtree._root[1] == 'Semi-eco: 5-10k':
                semi_eco += 1
            elif subtree._root[1] == 'Semi-buy: 10-20k':
                semi_buy += 1
            else:
                full += 1

    def best_buy_for_map(self, map_played: str) -> str:
        """
        Returns a string stating which buy type is more likely to win based on the given map (map_played).
        The buy types are:
        - Eco-buy
        - Semi-eco
        - Semi-buy
        - Full buy
        Result is determined based on the data from self.
        """
        eco = 0
        semi_eco = 0
        semi_buy = 0
        full = 0
        for subtree1 in self._subtrees:
            for subtree2 in subtree1._subtrees:
                for subtree3 in subtree2._subtrees:
                    if subtree3._root.lower() == map_played:
                        for subtree4 in subtree3._subtrees:
                            subtree4._best_buy_helper(eco, semi_eco, semi_buy, full)
        all_buys = [eco, semi_eco, semi_buy, full]
        if max(all_buys) == eco:
            return 'Eco buy is most effective'
        elif max(all_buys) == semi_eco:
            return 'Semi-eco buy is most effective'
        elif max(all_buys) == semi_buy:
            return 'Semi-buy is most effective'
        else:
            return 'Full buy is most effective'

    def combine_all(self, trees: list) -> None:
        """
        Combines all the trees in the input "trees" into one, where each tree corresponds to one year of the
        tournament.
        """
        for tree in trees:
            self._subtrees.append(tree)


def read_game(game_data: TextIO) -> tuple[str, list[dict]]:
    """
    Returns a tuple consisting of the year a tournament took place and all the information needed to create a tree
    representation of the data.
    game_data is a csv file with the information of one year's Valorant tournament, specifically with the
    attacker/defender scores of every winning team.
    Each dictionary in the returned list (in the tuple) corresponds to the information of a game in the tournament.
    """
    info = []
    game_data.readline()
    line = game_data.readline().strip().split(',')

    year = line[0].split()[2]

    while line[0] != '':
        game = {}
        matches = {}
        match_name = line[3]
        match_map = line[4]
        team_a, team_b = line[5], line[10]
        teama_attack, teama_defend = int(line[7]), int(line[8])
        teamb_attack, teamb_defend = int(line[12]), int(line[13])
        matches[match_map] = {team_a: (teama_attack, teama_defend), team_b: (teamb_attack, teamb_defend)}

        line = game_data.readline().strip().split(',')
        while line[0] != '' and line[3] == match_name:
            match_map = line[4]
            team_a, team_b = line[5], line[10]
            teama_attack, teama_defend = int(line[7]), int(line[8])
            teamb_attack, teamb_defend = int(line[12]), int(line[13])
            matches[match_map] = {team_a: (teama_attack, teama_defend), team_b: (teamb_attack, teamb_defend)}
            line = game_data.readline().strip().split(',')

        game[match_name] = matches
        info.append(game)
    return (year, info)


def read_buy_type(eco_data: TextIO) -> tuple[str, list[dict]]:
    """
    Returns a tuple consisting of the year a tournament took place and all the information needed to create a tree
    representation of the data.
    eco_data is a csv file with the information of one year's Valorant tournament, specifically with the buy type of
    each winning team.
    Each dictionary in the returned list represents a game in the tournament and all of its buy type information.
    """
    info = []
    eco_data.readline()
    line = eco_data.readline().strip().split(',')

    year = line[0].split()[2]

    while line[0] != '':
        game = {}
        matches = {}
        match_name = line[3]
        match_map = line[4]
        round_num = int(line[5])

        outcome = line[10]
        if outcome == 'Loss':
            line = eco_data.readline().strip().split(',')
            winning_team = line[6]
            type_buy = line[9]
            matches[match_map] = {round_num: (winning_team, type_buy)}
        else:
            winning_team = line[6]
            type_buy = line[9]
            matches[match_map] = {round_num: (winning_team, type_buy)}
            eco_data.readline().strip().split(',')

        line = eco_data.readline().strip().split(',')
        while line[0] != '' and line[3] == match_name:
            match_map = line[4]
            if match_map in matches:
                if line[10] == 'Loss':
                    line = eco_data.readline().strip().split(',')
                    matches[match_map][int(line[5])] = (line[6], line[9])
                else:
                    matches[match_map][int(line[5])] = (line[6], line[9])
                    eco_data.readline().strip().split(',')
            else:
                if line[10] == 'Loss':
                    line = eco_data.readline().strip().split(',')
                    matches[match_map] = {int(line[5]): (line[6], line[9])}
                else:
                    matches[match_map] = {int(line[5]): (line[6], line[9])}
                    eco_data.readline().strip().split(',')
            line = eco_data.readline().strip().split(',')

        game[match_name] = matches
        info.append(game)
    return (year, info)


def generate_tree(data: tuple[str, list[dict]]) -> Tree:
    """
    Creates a tree representation of the given data.
    data represents the results of either read_buy_type or read_game for a given year.
    """
    t = Tree(f"VCT {data[0]}", [])
    for game in data[1]:
        keys = list(game.keys())
        match = keys[0]
        for m_map in game[match]:
            for team in game[match][m_map]:
                items = [match, m_map, team, game[match][m_map][team]]
                t.insert_sequence(items)
    return t


def visualize_tree_game(data1: list[dict], data2: list[dict], data3: list[dict]) -> Figure:
    """
    Returns a tree in the Figure class object from the following data of attack/defender scores given as lists of
    dictionary. data1 represents the data from 2021, data2 represents the data from 2022, and data3 represents the data
    from 2023.

    Parts of the code is taken from: https://stackoverflow.com/questions/77214598/how-do-i-flip-my-igraph-
    tree-in-python-so-that-it-isnt-upside-down
    """
    i_d = 0
    g = Graph(directed=True)
    g.add_vertex('VCT')

    id_1 = visual_tree_game_helper(g, i_d, data1, '2021')
    id_2 = visual_tree_game_helper(g, id_1, data2, '2022')
    visual_tree_game_helper(g, id_2, data3, '2023')

    layt = g.layout("kk")

    edge_x, edge_y = [], []
    for edge in g.get_edgelist():
        x0, y0 = layt[edge[0]]
        x1, y1 = layt[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Get vertex coordinates and labels
    node_x, node_y = zip(*[layt[vertex] for vertex in g.vs.indices])
    # node_labels = [str(label) for label in g.vs.indices]
    node_labels = g.vs['name']

    # Create Plotly trace for edges
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line={"width": 0.5, "color": '#888'},
        hoverinfo="none",
        mode="lines",
    )

    # Create Plotly trace for nodes
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker={"showscale": True, "colorscale": 'YlGnBu', "size": 10},
        text=node_labels,  # Display node labels on hover
    )

    # Create a figure and add traces
    fig = go.Figure(data=[edge_trace, node_trace])

    # Customize layout
    fig.update_layout(
        showlegend=True,
        hovermode="closest",
        margin={"b": 0, "l": 0, "r": 0, "t": 0},
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
    )

    # Show the interactive plot
    return fig


def visual_tree_game_helper(g: Graph, cur_id: int, data: list[dict], year: str) -> int:
    """
    A helper function that returns the latest id for each node so that each node is distinguished from the other nodes.
    This function adds the vertices and the edges between them. This function is used alongside the visualize_tree_game
    function. The function takes in a graph, the current id, the data that is worked with, and the year of the data.
    """
    g.add_vertex('VCT ' + year)
    g.add_edge('VCT', 'VCT ' + year)
    for game in data:
        name_of_match = list(game.keys())[0]
        maps = list(game[name_of_match].keys())
        g.add_vertex(name_of_match + ' id: ' + str(cur_id))
        g.add_edge(name_of_match + ' id: ' + str(cur_id), 'VCT ' + year)
        name_of_match_id = cur_id
        for m in maps:
            team_name = list(game[name_of_match][m])
            team1 = team_name[0]
            team2 = team_name[1]
            team1attack, team1defend = (list(game[name_of_match][m].values())[0][0],
                                        list(game[name_of_match][m].values())[0][1])
            team2attack, team2defend = (list(game[name_of_match][m].values())[1][0],
                                        list(game[name_of_match][m].values())[1][1])
            cur_id += 1
            team1_id = cur_id
            g.add_vertex(team1 + ' id: ' + str(cur_id))
            g.add_vertex(str(team1attack) + ' attack by ' + team1 + ' id: ' + str(cur_id))
            g.add_vertex(str(team1defend) + ' defend by ' + team1 + ' id: ' + str(cur_id))
            g.add_edge(team1 + ' id: ' + str(cur_id), str(team1attack) + ' attack by ' + team1 + ' id: ' + str(cur_id))
            g.add_edge(team1 + ' id: ' + str(cur_id), str(team1defend) + ' defend by ' + team1 + ' id: ' + str(cur_id))
            cur_id += 1
            team2_id = cur_id
            g.add_vertex(team2 + ' id: ' + str(cur_id))
            g.add_vertex(str(team2attack) + ' attack by ' + team2 + ' id: ' + str(cur_id))
            g.add_vertex(str(team2defend) + ' defend by ' + team2 + ' id: ' + str(cur_id))
            g.add_edge(team2 + ' id: ' + str(cur_id), str(team2attack) + ' attack by ' + team2 + ' id: ' + str(cur_id))
            g.add_edge(team2 + ' id: ' + str(cur_id), str(team2defend) + ' defend by ' + team2 + ' id: ' + str(cur_id))
            cur_id += 1
            g.add_vertex(m + ' id: ' + str(cur_id))
            g.add_edge(m + ' id: ' + str(cur_id), team1 + ' id: ' + str(team1_id))
            g.add_edge(m + ' id: ' + str(cur_id), team2 + ' id: ' + str(team2_id))
            g.add_edge(m + ' id: ' + str(cur_id), name_of_match + ' id: ' + str(name_of_match_id))
        cur_id += 1
    return cur_id + 1


def visualize_tree_eco(data1: list[dict], data2: list[dict], data3: list[dict]) -> Figure:
    """
    Returns a tree in the Figure class object from the following data of buy types given as lists of
    dictionary. data1 represents the data from 2021, data2 represents the data from 2022, and data3 represents the data
    from 2023.

    Parts of the code is taken from: https://stackoverflow.com/questions/77214598/how-do-i-flip-my-igraph-tree-
    in-python-so-that-it-isnt-upside-down
    """
    i_d = 0
    g = Graph(directed=True)
    g.add_vertex('VCT')

    id_1 = visual_tree_econ_helper(g, i_d, data1, '2021')
    id_2 = visual_tree_econ_helper(g, id_1, data2, '2022')
    visual_tree_econ_helper(g, id_2, data3, '2023')

    layt = g.layout("kk")

    edge_x, edge_y = [], []
    for edge in g.get_edgelist():
        x0, y0 = layt[edge[0]]
        x1, y1 = layt[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Get vertex coordinates and labels
    node_x, node_y = zip(*[layt[vertex] for vertex in g.vs.indices])
    # node_labels = [str(label) for label in g.vs.indices]
    node_labels = g.vs['name']

    # Create Plotly trace for edges
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line={"width": 0.5, "color": '#888'},
        hoverinfo="none",
        mode="lines",
    )

    # Create Plotly trace for nodes
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker={"showscale": True, "colorscale": 'YlGnBu', "size": 10},
        text=node_labels,  # Display node labels on hover
    )

    # Create a figure and add traces
    fig = go.Figure(data=[edge_trace, node_trace])

    # Customize layout
    fig.update_layout(
        showlegend=True,
        hovermode="closest",
        margin={"b": 0, "l": 0, "r": 0, "t": 0},
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
    )

    # Show the interactive plot
    return fig


def visual_tree_econ_helper(g: Graph, cur_id: int, data: list[dict], year: str) -> int:
    """
    A helper function that returns the latest id for each node so that each node is distinguished from the other nodes.
    This function adds the vertices and the edges between them. This function is used alongside the visualize_tree_eco
    function. The function takes in a graph, the current id, the data that is worked with, and the year of the data.
    """
    g.add_vertex('VCT ' + year)
    g.add_edge('VCT', 'VCT ' + year)
    for game in data:
        name_of_match = list(game.keys())[0]
        maps = list(game[name_of_match].keys())
        g.add_vertex(name_of_match + ' id: ' + str(cur_id))
        g.add_edge(name_of_match + ' id: ' + str(cur_id), 'VCT ' + year)
        name_of_match_id = cur_id
        for m in maps:
            cur_id += 1
            map_id = cur_id
            g.add_vertex(m + ' id: ' + str(map_id))
            for matches in game[name_of_match][m].values():
                cur_id += 1
                g.add_vertex(matches[0] + ' won by ' + matches[1] + ' id: ' + str(cur_id))
                g.add_edge(matches[0] + ' won by ' + matches[1] + ' id: ' + str(cur_id), m + ' id: ' + str(map_id))
            g.add_edge(m + ' id: ' + str(map_id), name_of_match + ' id: ' + str(name_of_match_id))
        cur_id += 1
    return cur_id + 1


# ---MAIN---
if __name__ == '__main__':
    if __name__ == '__main__':
        game_datas = []
        eco_datas = []
        game_trees, eco_trees = [], []
        for x in range(1, 4):
            with open('tree_data/maps_scores_202' + str(x) + '.csv') as game_file:
                game_dat = read_game(game_file)

            with open('tree_data/eco_data_202' + str(x) + '.csv') as eco_file:
                eco_dat = read_buy_type(eco_file)

            game_datas.append(game_dat)
            eco_datas.append(eco_dat)
            game_trees.append(generate_tree(game_dat))
            eco_trees.append(generate_tree(eco_dat))

        vct_tree = Tree('VCT', [])
        vct_tree.combine_all(game_trees)

        eco_tree = Tree('VCT buy types', [])
        eco_tree.combine_all(eco_trees)

        current_map = input("What map are you playing?").lower()
        print("This map " + vct_tree.best_side_for_map(current_map))
        print(eco_tree.best_buy_for_map(current_map))
        visualize_tree_game(game_datas[0][1], game_datas[1][1], game_datas[2][1])
        visualize_tree_eco(eco_datas[0][1], eco_datas[1][1], eco_datas[2][1])

        import doctest

        doctest.testmod()
        import python_ta

        python_ta.check_all(config={
            'max-line-length': 120,
            'extra-imports': ['igraph', 'plotly.graph_objects', 'plotly.graph_objs', 'dash.html'],
            'allowed-io': [],
            'max-nested-blocks': 5
        })

    # visualize_tree_eco(eco_data_2021[1], eco_data_2022[1], eco_data_2023[1])
    # visualize_tree_game(game_data_2021[1], game_data_2022[1], game_data_2023[1])
