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

    def make_tree(self, data: list[dict]) -> Tree:
        """
        TODO: docstring
        :param data:
        :return:
        """
    # functions that read graph_data from file (returns list or dict or list of list?):
    # teams, matches (with map as item??), defense or attack win

    # function that takes in graph_data (list or dict) and creates the tree

    # then traverse the tree to get "most likely to win" stuff (figure that out later)


def read_game(game_data: TextIO) -> list[dict]:
    """
    TODO: docstring
    :param game_data:
    :return:
    """
    info = []
    game_data.readline()
    line = game_data.readline().strip().split(',')
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
            matches[match_map] = {line[5]: (int(line[7]), int(line[8])), line[10]: int((line[12]), int(line[13]))}
            line = game_data.readline().strip().split(',')

        game[match_name] = matches
        info.append(game)
    return info


def read_buy_type(eco_data: TextIO) -> list[dict]:
    """
    TODO: docstring
    :param eco_data:
    :return:
    """
    info = []
    eco_data.readline()
    line = eco_data.readline().strip().split(',')
    while line[0] != '':
        game = {}
        matches = {}
        match_name = line[3]
        match_map = line[4]
        round_num = int(line[5])

        outcome = line[10]
        if outcome == 'loss':
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
            while line[0] != '' and line[4] == match_map:
                if line[10] == 'loss':
                    line = eco_data.readline().strip().split(',')
                    matches[match_map][int(line[5])] = (line[6], line[9])
                else:
                    matches[match_map][int(line[5])] = (line[6], line[9])
                    eco_data.readline().strip().split(',')
                line = eco_data.readline().strip().split(',')
            match_map = line[4]
            if line[10] == 'loss':
                line = eco_data.readline().strip().split(',')
                matches[match_map] = {int(line[5]): (line[6], line[9])}
            else:
                matches[match_map] = {int(line[5]): (line[6], line[9])}
                eco_data.readline().strip().split(',')
            line = eco_data.readline().strip().split(',')

        game[match_name] = matches
        info.append(game)

    return info

# Tournament,Stage,Match Type,Match Name,Map,Round Number,Team,Loadout Value,Remaining Credits,Type,Outcome
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,1,Vision Strikers,3.9k,0.4k,Eco: 0-5k,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,1,FULL SENSE,3.4k,0.2k,Eco: 0-5k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,2,Vision Strikers,14.4k,5.2k,Semi-buy: 10-20k,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,2,FULL SENSE,2.4k,8.4k,Eco: 0-5k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,3,Vision Strikers,17.6k,15.2k,Semi-buy: 10-20k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,3,FULL SENSE,19.9k,0.9k,Semi-buy: 10-20k,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,4,Vision Strikers,22.6k,4.7k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,4,FULL SENSE,21.7k,9.0k,Full buy: 20k+,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,5,Vision Strikers,22.0k,4.2k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,5,FULL SENSE,10.0k,10.2k,Semi-buy: 10-20k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,6,Vision Strikers,23.0k,17.1k,Full buy: 20k+,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,6,FULL SENSE,21.9k,2.0k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,7,Vision Strikers,22.6k,5.5k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,7,FULL SENSE,21.3k,7.4k,Full buy: 20k+,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,8,Vision Strikers,22.0k,4.9k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,8,FULL SENSE,8.1k,10.3k,Semi-eco: 5-10k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,9,Vision Strikers,23.1k,11.2k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,9,FULL SENSE,21.6k,1.4k,Full buy: 20k+,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,10,Vision Strikers,22.6k,16.9k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Haven,10,FULL SENSE,14.3k,6.8k,Semi-buy: 10-20k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,1,Vision Strikers,3.6k,0.5k,Eco: 0-5k,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,1,FULL SENSE,3.9k,0.1k,Eco: 0-5k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,2,Vision Strikers,14.0k,5.5k,Semi-buy: 10-20k,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,2,FULL SENSE,2.3k,8.0k,Eco: 0-5k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,3,Vision Strikers,19.5k,14.8k,Semi-buy: 10-20k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,3,FULL SENSE,20.3k,0.2k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,4,Vision Strikers,23.5k,3.7k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,4,FULL SENSE,19.7k,5.0k,Semi-buy: 10-20k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,5,Vision Strikers,24.3k,15.5k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,5,FULL SENSE,7.9k,10.3k,Semi-eco: 5-10k,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,6,Vision Strikers,25.4k,18.4k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,6,FULL SENSE,21.8k,1.8k,Full buy: 20k+,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,7,Vision Strikers,24.5k,29.7k,Full buy: 20k+,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,7,FULL SENSE,13.3k,5.9k,Semi-buy: 10-20k,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,8,Vision Strikers,22.9k,18.1k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,8,FULL SENSE,24.9k,12.9k,Full buy: 20k+,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,9,Vision Strikers,24.6k,27.6k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,9,FULL SENSE,24.6k,4.9k,Full buy: 20k+,Loss
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,10,Vision Strikers,24.6k,27.6k,Full buy: 20k+,Win
# Valorant Champions 2021,Group Stage,Opening (D),Vision Strikers vs FULL SENSE,Breeze,10,FULL SENSE,10.7k,8.2k,Semi-buy: 10-20k,Loss
