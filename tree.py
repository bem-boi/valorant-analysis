"""
trees r slay
"""
from __future__ import annotations
from typing import Any, Optional, TextIO
from igraph import Graph
import plotly.graph_objects as go
from plotly.graph_objs import Figure


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

    def get_root(self) -> Optional[Any]:
        """Returns the root of this tree"""
        return self._root

    def get_subtrees(self) -> Optional[Any]:
        """Returns the subtrees of this tree"""
        return self._subtrees

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

    def __contains__(self, item: Any) -> bool:
        """Return whether the given is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.__contains__(1)
        True
        >>> t.__contains__(5)
        True
        >>> t.__contains__(4)
        False
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def __repr__(self) -> str:
        """Return a one-line string representation of this tree.

        >>> t = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> t
        Tree(2, [Tree(4, []), Tree(5, [])])
        """
        return f"Tree({self._root}, {self._subtrees})"

    def height(self: Tree) -> int:
        """Return the height of this tree.

        Please refer to the prep readings for the definition of tree height.

        >>> t1 = Tree(17, [])
        >>> t1.height()
        1
        >>> t2 = Tree(1, [Tree(4, [Tree(5, [])]), Tree(1, [Tree(5, [Tree(5, [])])])])
        >>> t2.height()
        4
        """
        if self.is_empty():
            return 0
        elif not self._subtrees:
            return 1
        else:
            max_height = 0
            for subtree in self._subtrees:
                if subtree.height() > max_height:
                    max_height = subtree.height()
            return 1 + max_height

    def insert_sequence(self, items: list) -> None:
        """Insert the given items into this tree.

        The inserted items form a chain of descendants, where:
            - items[0] is a child of this tree's root
            - items[1] is a child of items[0]
            - items[2] is a child of items[1]
            - etc.

        Do nothing if items is empty.

        The root of this chain (i.e. items[0]) should be added as a new subtree within this tree, as long as items[0]
        does not already exist as a child of the current root node. That is, create a new subtree for it
        and append it to this tree's existing list of subtrees.

        If items[0] is already a child of this tree's root, instead recurse into that existing subtree rather
        than create a new subtree with items[0]. If there are multiple occurrences of items[0] within this tree's
        children, pick the left-most subtree with root value items[0] to recurse into.

        Hints:

        To do this recursively, you'll need to recurse on both the tree argument
        (from self to a subtree) AND on the given items, using the "first" and "rest" idea
        from RecursiveLists. To access the "rest" of a built-in Python list, you can use
        list slicing: items[1:len(items)] or simply items[1:], or you can use a recursive helper method
        that takes an extra "current index" argument to keep track of the next move in the list to add.

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

    def best_side_for_map(self, map_played: str) -> str:
        """
        TODO: docstring
        :param map_played:
        :return:
        """
        attack = 0
        defend = 0
        for subtree1 in self._subtrees:
            for subtree2 in subtree1._subtrees:
                if subtree2._root.lower() == map_played:
                    for subtree3 in subtree2._subtrees:
                        for subtree4 in subtree3._subtrees:
                            for subtree5 in subtree4._subtrees:
                                attack += subtree5._root[0]
                                defend += subtree5._root[1]
        if attack > defend:
            return "Attacker sided"
        if attack < defend:
            return "Defender sided"
        else:
            return "Map favours both sides"

    def best_buy_for_map(self, map_played: str) -> str:
        """
        Returns a message stating the type of buy that is best for map_played
        """
        eco = 0
        semi_eco = 0
        semi_buy = 0
        full = 0
        for subtree1 in self._subtrees:
            for subtree2 in subtree1._subtrees:
                if subtree2._root.lower() == map_played:
                    for subtree3 in subtree2._subtrees:
                        for subtree4 in subtree3._subtrees:
                            for subtree5 in subtree4._subtrees:
                                if subtree5._root[1] == 'Eco: 0-5k':
                                    eco += 1
                                elif subtree5._root[1] == 'Semi-eco: 5-10k':
                                    semi_eco += 1
                                elif subtree5._root[1] == 'Semi-buy: 10-20k':
                                    semi_buy += 1
                                else:
                                    full += 1
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
        TODO: docstring
        :param trees:
        :return:
        """
        for tree in trees:
            self._subtrees.append(tree)


def read_game(game_data: TextIO) -> tuple[str, list[dict]]:
    """
    TODO: docstring
    :param game_data:
    :return:
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
    return year, info


def read_buy_type(eco_data: TextIO) -> tuple[str, list[dict]]:
    """
    TODO: docstring
    :param eco_data:
    :return:
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
    return year, info


def generate_tree(data: tuple[str, list[dict]]) -> Tree:
    """
    TODO: docstring
    :param data:
    :return:
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


def data_at_height(t: Tree, i: int) -> list:
    """
    Returns a list of the values of the nodes at depth i of the tree t
    (the root node is considered to have a depth of 0)

    Preconditions:
        - i >= 0

    >>> t1 = Tree(1, [Tree(4, [Tree(5, [])]), Tree(1, [Tree(5, [Tree(5, [])])])])
    >>> data_at_height(t1, 0)
    [1]
    >>> data_at_height(t1, 2)
    [5, 5]
    >>> t2 = Tree(1, [Tree(2, [Tree(4, []),Tree(5, [])]),Tree(3, [Tree(6, []),Tree(7, [])])])
    >>> data_at_height(t2, 2)
    [4, 5, 6, 7]
    """
    if i == 0:
        return [t.get_root()] if t.get_root() is not None else []
    else:
        nodes = []
        for subtree in t.get_subtrees():
            nodes.extend(data_at_height(subtree, i - 1))
        return nodes


def visualize_tree(data1: list[dict], data2: list[dict], data3: list[dict]) -> Figure:
    """
    Returns a tree from the following data given as a Figure class object
    """
    i_d = 0
    g = Graph(directed=True)
    g.add_vertex('VCT')
    g.add_vertex('VCT 2021')
    g.add_edge('VCT', 'VCT 2021')
    for game in data1:
        name_of_match = list(game.keys())[0]
        maps = list(game[name_of_match].keys())
        g.add_vertex(name_of_match + ' id: ' + str(i_d))
        g.add_edge(name_of_match + ' id: ' + str(i_d), 'VCT 2021')
        name_of_match_id = i_d
        for m in maps:
            team_name = list(game[name_of_match][m])
            team1 = team_name[0]
            team2 = team_name[1]
            team1attack, team1defend = (list(game[name_of_match][m].values())[0][0],
                                        list(game[name_of_match][m].values())[0][1])
            team2attack, team2defend = (list(game[name_of_match][m].values())[1][0],
                                        list(game[name_of_match][m].values())[1][1])
            i_d += 1
            team1_id = i_d
            g.add_vertex(team1 + ' id: ' + str(i_d))
            g.add_vertex(str(team1attack) + ' attack by ' + team1 + ' id: ' + str(i_d))
            g.add_vertex(str(team1defend) + ' defend by ' + team1 + ' id: ' + str(i_d))
            g.add_edge(team1 + ' id: ' + str(i_d), str(team1attack) + ' attack by ' + team1 + ' id: ' + str(i_d))
            g.add_edge(team1 + ' id: ' + str(i_d), str(team1defend) + ' defend by ' + team1 + ' id: ' + str(i_d))
            i_d += 1
            team2_id = i_d
            g.add_vertex(team2 + ' id: ' + str(i_d))
            g.add_vertex(str(team2attack) + ' attack by ' + team2 + ' id: ' + str(i_d))
            g.add_vertex(str(team2defend) + ' defend by ' + team2 + ' id: ' + str(i_d))
            g.add_edge(team2 + ' id: ' + str(i_d), str(team2attack) + ' attack by ' + team2 + ' id: ' + str(i_d))
            g.add_edge(team2 + ' id: ' + str(i_d), str(team2defend) + ' defend by ' + team2 + ' id: ' + str(i_d))
            i_d += 1
            g.add_vertex(m + ' id: ' + str(i_d))
            g.add_edge(m + ' id: ' + str(i_d), team1 + ' id: ' + str(team1_id))
            g.add_edge(m + ' id: ' + str(i_d), team2 + ' id: ' + str(team2_id))
            g.add_edge(m + ' id: ' + str(i_d), name_of_match + ' id: ' + str(name_of_match_id))
        i_d += 1

    g.add_vertex('VCT 2022')
    g.add_edge('VCT', 'VCT 2022')
    for game in data1:
        name_of_match = list(game.keys())[0]
        maps = list(game[name_of_match].keys())
        g.add_vertex(name_of_match + ' id: ' + str(i_d))
        g.add_edge(name_of_match + ' id: ' + str(i_d), 'VCT 2022')
        name_of_match_id = i_d
        for m in maps:
            team_name = list(game[name_of_match][m])
            team1 = team_name[0]
            team2 = team_name[1]
            team1attack, team1defend = (list(game[name_of_match][m].values())[0][0],
                                        list(game[name_of_match][m].values())[0][1])
            team2attack, team2defend = (list(game[name_of_match][m].values())[1][0],
                                        list(game[name_of_match][m].values())[1][1])
            i_d += 1
            team1_id = i_d
            g.add_vertex(team1 + ' id: ' + str(i_d))
            g.add_vertex(str(team1attack) + ' attack by ' + team1 + ' id: ' + str(i_d))
            g.add_vertex(str(team1defend) + ' defend by ' + team1 + ' id: ' + str(i_d))
            g.add_edge(team1 + ' id: ' + str(i_d), str(team1attack) + ' attack by ' + team1 + ' id: ' + str(i_d))
            g.add_edge(team1 + ' id: ' + str(i_d), str(team1defend) + ' defend by ' + team1 + ' id: ' + str(i_d))
            i_d += 1
            team2_id = i_d
            g.add_vertex(team2 + ' id: ' + str(i_d))
            g.add_vertex(str(team2attack) + ' attack by ' + team2 + ' id: ' + str(i_d))
            g.add_vertex(str(team2defend) + ' defend by ' + team2 + ' id: ' + str(i_d))
            g.add_edge(team2 + ' id: ' + str(i_d), str(team2attack) + ' attack by ' + team2 + ' id: ' + str(i_d))
            g.add_edge(team2 + ' id: ' + str(i_d), str(team2defend) + ' defend by ' + team2 + ' id: ' + str(i_d))
            i_d += 1
            g.add_vertex(m + ' id: ' + str(i_d))
            g.add_edge(m + ' id: ' + str(i_d), team1 + ' id: ' + str(team1_id))
            g.add_edge(m + ' id: ' + str(i_d), team2 + ' id: ' + str(team2_id))
            g.add_edge(m + ' id: ' + str(i_d), name_of_match + ' id: ' + str(name_of_match_id))
        i_d += 1

    g.add_vertex('VCT 2023')
    g.add_edge('VCT', 'VCT 2023')
    for game in data1:
        name_of_match = list(game.keys())[0]
        maps = list(game[name_of_match].keys())
        g.add_vertex(name_of_match + ' id: ' + str(i_d))
        g.add_edge(name_of_match + ' id: ' + str(i_d), 'VCT 2023')
        name_of_match_id = i_d
        for m in maps:
            team_name = list(game[name_of_match][m])
            team1 = team_name[0]
            team2 = team_name[1]
            team1attack, team1defend = (list(game[name_of_match][m].values())[0][0],
                                        list(game[name_of_match][m].values())[0][1])
            team2attack, team2defend = (list(game[name_of_match][m].values())[1][0],
                                        list(game[name_of_match][m].values())[1][1])
            i_d += 1
            team1_id = i_d
            g.add_vertex(team1 + ' id: ' + str(i_d))
            g.add_vertex(str(team1attack) + ' attack by ' + team1 + ' id: ' + str(i_d))
            g.add_vertex(str(team1defend) + ' defend by ' + team1 + ' id: ' + str(i_d))
            g.add_edge(team1 + ' id: ' + str(i_d), str(team1attack) + ' attack by ' + team1 + ' id: ' + str(i_d))
            g.add_edge(team1 + ' id: ' + str(i_d), str(team1defend) + ' defend by ' + team1 + ' id: ' + str(i_d))
            i_d += 1
            team2_id = i_d
            g.add_vertex(team2 + ' id: ' + str(i_d))
            g.add_vertex(str(team2attack) + ' attack by ' + team2 + ' id: ' + str(i_d))
            g.add_vertex(str(team2defend) + ' defend by ' + team2 + ' id: ' + str(i_d))
            g.add_edge(team2 + ' id: ' + str(i_d), str(team2attack) + ' attack by ' + team2 + ' id: ' + str(i_d))
            g.add_edge(team2 + ' id: ' + str(i_d), str(team2defend) + ' defend by ' + team2 + ' id: ' + str(i_d))
            i_d += 1
            g.add_vertex(m + ' id: ' + str(i_d))
            g.add_edge(m + ' id: ' + str(i_d), team1 + ' id: ' + str(team1_id))
            g.add_edge(m + ' id: ' + str(i_d), team2 + ' id: ' + str(team2_id))
            g.add_edge(m + ' id: ' + str(i_d), name_of_match + ' id: ' + str(name_of_match_id))
        i_d += 1

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


def create_tree_from_edges(edges: Any) -> Graph:
    """
    Returns a tree made from the edges given as an igraph Graph object
    """

    # from igraph import plot (NO need; igraph already imported at top)
    # import cairocffi
    # Create an empty directed graph
    tree = Graph(directed=True)
    # Add vertices
    vertices = set()
    for edge in edges:
        vertices.update(edge)
    tree.add_vertices(list(vertices))
    # Add edges to the graph
    tree.add_edges(edges)
    return tree


# --------------------------------------------------- MAIN ---------------------------------------------------------- #
if __name__ == '__main__':
    game_datas = []
    game_trees, eco_trees = [], []
    for x in range(1, 4):
        with open('tree_data/testy_test.txt') as game_file:
            # after testing replace 'tree_data/testy_test.txt' with 'tree_data/maps_scores_202' + str(x) + '.csv'
            game_dat = read_game(game_file)

        with open('tree_data/testy_test_eco.txt') as eco_file:
            # after testing replace 'tree_data/testy_test.txt' with 'tree_data/eco_rounds_202' + str(x) + '.csv'
            eco_dat = read_buy_type(eco_file)

        game_datas.append(game_dat)
        game_trees.append(generate_tree(game_dat))
        eco_trees.append(generate_tree(eco_dat))

    vct_tree = Tree('VCT', [])
    vct_tree.combine_all(game_trees)

    eco_tree = Tree('VCT buy types', [])
    eco_tree.combine_all(eco_trees)

    # current_map = input("What map are you playing?").lower()
    # print("This map is " + vct_tree.best_side_for_map(current_map))
    # print(eco_tree.best_buy_for_map(current_map))
    visualize_tree(game_datas[0][1], game_datas[0][1], game_datas[0][1])

    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['igraph', 'plotly.graph_objects', 'plotly.graph_objs'],
        'allowed-io': [],
        'max-nested-blocks': 5
    })
