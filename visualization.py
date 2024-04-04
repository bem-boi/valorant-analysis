"""
Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team

We amended this source code from ex4_visualization.py
"""
from typing import Any
import networkx as nx
from plotly.graph_objs import Scatter, Figure

from graph import WeightedGraph

# Colours to use when visualizing different clusters.
COLOUR_SCHEME = [
    '#2E91E5', '#E15F99', '#1CA71C', '#FB0D0D', '#DA16FF', '#222A2A', '#B68100',
    '#750D86', '#EB663B', '#511CFB', '#00A08B', '#FB00D1', '#FC0080', '#B2828D',
    '#6C7C32', '#778AAE', '#862A16', '#A777F1', '#620042', '#1616A7', '#DA60CA',
    '#6C4516', '#0D2A63', '#AF0038'
]

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
MAP_COLOUR = 'rgb(89, 205, 105)'
AGENT_COLOUR = 'rgb(105, 89, 205)'


def setup_weighted_graph(graph: WeightedGraph, layout: str = 'spring_layout',
                         max_vertices: int = 5000) -> list:
    """
    Use plotly and networkx to set up the visuals for the given graph.
    """

    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)
    weights = nx.get_edge_attributes(graph_nx, 'weight')

    positions = set_weights(graph_nx, pos, weights)

    types = [graph_nx.nodes[k]['type'] for k in graph_nx.nodes]

    colours = [MAP_COLOUR if vertex_type == 'map' else AGENT_COLOUR for vertex_type in types]

    trace3 = Scatter(x=positions[0],
                     y=positions[1],
                     mode='lines+text',
                     name='edges',
                     line={"color": LINE_COLOUR, "width": 1},
                     )

    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker={"symbol": 'circle-dot',
                             "size": 5,
                             "color": colours,
                             "line": {"color": VERTEX_BORDER_COLOUR, "width": 0.5}
                             },
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    return [positions[2], [trace3, trace4]]


def visualize_weighted_graph(graph: WeightedGraph,
                             layout: str = 'spring_layout',
                             max_vertices: int = 5000,
                             output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given weighted graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """

    weight_positions, data = setup_weighted_graph(graph, layout, max_vertices)
    draw_weighted_graph(data, weight_positions, output_file)


def return_weighted_graph(graph: WeightedGraph, layout: str = 'spring_layout',
                          max_vertices: int = 5000) -> Figure:
    """
    Returns the weighted graph given as a Figure class object
    """
    weight_positions, data = setup_weighted_graph(graph, layout, max_vertices)
    fig = Figure(data=data)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    for w in weight_positions:
        fig.add_annotation(
            x=w[0], y=w[1],  # Text annotation position
            xref="x", yref="y",  # Coordinate reference system
            text=w[2],  # Text content
            showarrow=False  # Hide arrow
        )

    return fig


def draw_weighted_graph(data: list, weight_positions: Any, output_file: str = '') -> None:
    """
    Draw a weighted graph based on given data
    where weight_positions are the weights to draw on edges for a weighted graph

    Optional arguments:
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """

    fig = Figure(data=data)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    for w in weight_positions:
        fig.add_annotation(
            x=w[0], y=w[1],  # Text annotation position
            xref="x", yref="y",  # Coordinate reference system
            text=w[2],  # Text content
            showarrow=False  # Hide arrow
        )

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)


def set_weights(g: nx.Graph, pos: Any, weights: dict) -> tuple:
    """
    Helper function for setup_weighted_graph to calculate the position of the edges and their weights
    """
    x_edges = []
    y_edges = []
    weight_positions = []

    for edge in g.edges:
        x1, x2 = pos[edge[0]][0], pos[edge[1]][0]
        x_edges += [x1, x2, None]
        y1, y2 = pos[edge[0]][1], pos[edge[1]][1]
        y_edges += [y1, y2, None]
        weight_positions.append(((x1 + x2) / 2, (y1 + y2) / 2, weights[(edge[0], edge[1])]))
    return x_edges, y_edges, weight_positions


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['networkx', 'plotly.graph_objs', 'graph'],
        'max-nested-blocks': 5
    })
