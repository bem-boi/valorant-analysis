"""
trees r slay
"""
from __future__ import annotations
from typing import Any, Optional, TextIO


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
        TODO: docstring
        :param map_played:
        :return:
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
    return (year, info)


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
    return (year, info)


def generate_tree(year: str, data: list[dict]) -> Tree:
    """
    TODO: docstring
    :param data:
    :return:
    """
    t = Tree('VCT ' + year, [])
    for game in data:
        keys = list(game.keys())
        match = keys[0]
        for m_map in game[match]:
            for team in game[match][m_map]:
                items = [match, m_map, team, game[match][m_map][team]]
                t.insert_sequence(items)
    return t


# ---MAIN---
if __name__ == '__main__':
    game_file_2021 = open('tree_data/maps_scores_2021.csv')
    game_file_2022 = open('tree_data/maps_scores_2022.csv')
    game_file_2023 = open('tree_data/maps_scores_2023.csv')

    eco_file_2021 = open('tree_data/eco_rounds_2021.csv')
    eco_file_2022 = open('tree_data/eco_rounds_2022.csv')
    eco_file_2023 = open('tree_data/eco_rounds_2023.csv')

    game_data_2021 = read_game(game_file_2021)
    game_data_2022 = read_game(game_file_2022)
    game_data_2023 = read_game(game_file_2023)

    eco_data_2021 = read_buy_type(eco_file_2021)
    eco_data_2022 = read_buy_type(eco_file_2022)
    eco_data_2023 = read_buy_type(eco_file_2023)

    game_tree_2021 = generate_tree(game_data_2021[0], game_data_2021[1])
    game_tree_2022 = generate_tree(game_data_2022[0], game_data_2022[1])
    game_tree_2023 = generate_tree(game_data_2023[0], game_data_2023[1])

    eco_tree_2021 = generate_tree(eco_data_2021[0], eco_data_2021[1])
    eco_tree_2022 = generate_tree(eco_data_2022[0], eco_data_2022[1])
    eco_tree_2023 = generate_tree(eco_data_2023[0], eco_data_2023[1])

    vct_tree = Tree('VCT', [])
    vct_tree.combine_all([game_tree_2021, game_tree_2022, game_tree_2023])

    eco_tree = Tree('VCT buy types', [])
    eco_tree.combine_all([eco_tree_2021, eco_tree_2022, eco_tree_2023])

    current_map = input("What map are you playing?").lower()
    print("This map is " + vct_tree.best_side_for_map(current_map))
    print(eco_tree.best_buy_for_map(current_map))
