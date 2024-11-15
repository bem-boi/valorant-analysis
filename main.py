from dash import Dash, dcc, html, Input, Output, callback, State, ctx

from graph import (clean_agents_pick_file, clean_teams_picked_agents_file, load_agent_role_data, load_map_agent_data,
                   generate_weighted_graph, return_graph, clean_all_agents_file, load_agent_combo_data,
                   compatible_agents, best_agent_for_map)

from tree import visualize_tree_game, read_game, read_buy_type, generate_tree, Tree, visualize_tree_eco


# INITIALIZE DATA FOR GRAPH #
cleaned_agf_file = clean_agents_pick_file('graph_data/agents_pick_rates2023.csv')
cleaned_tpa_file = clean_teams_picked_agents_file('graph_data/teams_picked_agents2023.csv')
cleaned_aa_file = clean_all_agents_file('graph_data/all_agents.csv')
agent_role_data = load_agent_role_data('graph_data/agent_roles.csv')
agent_combinations = load_agent_combo_data(cleaned_aa_file)
map_agent_data = load_map_agent_data(cleaned_agf_file, cleaned_tpa_file, agent_role_data)
map_agent_graph = generate_weighted_graph(map_agent_data, agent_combinations, view_agent_weights=True)


# INITIALIZE DATA FOR TREE #
game_file_2021_vis = open('tree_data/maps_scores_2021_visual.csv')
game_file_2022_vis = open('tree_data/maps_scores_2022_visual.csv')
game_file_2023_vis = open('tree_data/maps_scores_2023_visual.csv')

eco_file_2021_vis = open('tree_data/eco_data_2021_visual.csv')
eco_file_2022_vis = open('tree_data/eco_data_2022_visual.csv')
eco_file_2023_vis = open('tree_data/eco_data_2023_visual.csv')

game_data_2021_vis = read_game(game_file_2021_vis)
game_data_2022_vis = read_game(game_file_2022_vis)
game_data_2023_vis = read_game(game_file_2023_vis)

eco_data_2021_vis = read_buy_type(eco_file_2021_vis)
eco_data_2022_vis = read_buy_type(eco_file_2022_vis)
eco_data_2023_vis = read_buy_type(eco_file_2023_vis)

game_file_2021 = open('tree_data/maps_scores_2021.csv')
game_file_2022 = open('tree_data/maps_scores_2022.csv')
game_file_2023 = open('tree_data/maps_scores_2023.csv')

eco_file_2021 = open('tree_data/eco_data_2021.csv')
eco_file_2022 = open('tree_data/eco_data_2022.csv')
eco_file_2023 = open('tree_data/eco_data_2023.csv')

game_data_2021 = read_game(game_file_2021)
game_data_2022 = read_game(game_file_2022)
game_data_2023 = read_game(game_file_2023)

eco_data_2021 = read_buy_type(eco_file_2021)
eco_data_2022 = read_buy_type(eco_file_2022)
eco_data_2023 = read_buy_type(eco_file_2023)

game_tree_2021 = generate_tree(game_data_2021)
game_tree_2022 = generate_tree(game_data_2022)
game_tree_2023 = generate_tree(game_data_2023)

eco_tree_2021 = generate_tree(eco_data_2021)
eco_tree_2022 = generate_tree(eco_data_2022)
eco_tree_2023 = generate_tree(eco_data_2023)

vct_tree = Tree('VCT', [])
vct_tree.combine_all([game_tree_2021, game_tree_2022, game_tree_2023])
eco_tree = Tree('VCT buy types', [])
eco_tree.combine_all([eco_tree_2021, eco_tree_2022, eco_tree_2023])

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Valorant Analysis App'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Which Agents to play', value='tab-1'),
        dcc.Tab(label='Most effective buy', value='tab-2'),
        dcc.Tab(label='Attacker or Defender-sided', value='tab-3')
    ]),
    html.Div(id='tabs-content')
])


@callback(Output('tabs-content', 'children'),
          Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Which Agents to play'),
            html.Hr(),
            dcc.RadioItems(
                ['hide_agent_weight', 'show_agent_weight'], 'hide_agent_weight',
                inline=True, id='choice0_1'),
            dcc.RadioItems(
                ['duelists',
                 'controllers',
                 'initiators',
                 'sentinels', 'all'], 'duelists', inline=True, id='choice1_1'),
            dcc.RadioItems(
                ['ascent',
                 'pearl',
                 'split',
                 'lotus',
                 'icebox',
                 'fracture',
                 'bind',
                 'haven', 'all'], 'ascent', inline=True, id='choice2_1'),
            dcc.Graph(figure={}, id='visual_graph_1'),
            html.Hr(),
            html.Div(dcc.Input(id='input_user_1', type='text')),
            html.Button('Submit', id='button_1'),
            html.Div(id='output-container-button_1',
                     children="Enter your teammates' agents in the form: (Agent1),(Agent2),...,(Agent4). "
                              "or leave it blank"),
            html.Hr(),
            html.Div(dcc.Input(id='input_agent_1', type='text')),
            html.Button('Submit', id='button2_1'),
            html.Div(id='output-container-button2_1',
                     children="Enter an agent you're playing and press submit")
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Most effective buy'),
            html.Hr(),
            dcc.RadioItems(
                ['ascent',
                 'pearl',
                 'split',
                 'lotus',
                 'icebox',
                 'fracture',
                 'bind',
                 'haven'], 'ascent', inline=True, id='choice2_2'),
            dcc.Graph(figure=visualize_tree_eco(eco_data_2021_vis[1], eco_data_2022_vis[1], eco_data_2023_vis[1])),
            html.Div(id='text_eco',
                     children=eco_tree.best_buy_for_map('ascent') + ' on ascent'),
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Attacker or Defender-sided'),
            html.Hr(),
            dcc.RadioItems(
                ['ascent',
                 'pearl',
                 'split',
                 'lotus',
                 'icebox',
                 'fracture',
                 'bind',
                 'haven'], 'ascent', inline=True, id='choice2_3'),
            dcc.Graph(figure=visualize_tree_game(game_data_2021_vis[1], game_data_2022_vis[1], game_data_2023_vis[1])),
            html.Div(id='text_ct',
                     children='ascent ' + vct_tree.best_side_for_map('ascent')),
        ])

    html.Div(id='tabs-content')


# --------------------------------------------- which agent to play ------------------------------------------------- #

@callback(
    Output(component_id='visual_graph_1', component_property='figure'),
    [Input('choice0_1', 'value'),
     Input(component_id='choice1_1', component_property='value'),
     Input(component_id='choice2_1', component_property='value')]
)
def update_graph(choice0, choice1, choice2):
    if choice0 == 'hide_agent_weight':
        fig = return_graph(map_agent_data, agent_combinations, choice1, choice2)
    else:
        fig = return_graph(map_agent_data, agent_combinations, choice1, choice2, view_agent_weights=True)
    return fig


@callback(
    Output('output-container-button_1', 'children'),
    [Input('choice1_1', 'value'),
     Input('choice2_1', 'value'),
     Input('button_1', 'n_clicks')],
    State('input_user_1', 'value'),
    prevent_initial_call=True)
def update_output(choice1, choice2, button, input):
    button_clicked = ctx.triggered_id
    if button_clicked == 'button_1':
        agents_so_far = 'The best agent to play on ' + choice2 + ' are '
        if choice1 == 'all':
            choice1 = ''
        if input is None:
            agents_so_far += str(
                list(best_agent_for_map(map_agent_graph, choice2, [], choice1).keys()))
        else:
            teammate_agents = input.split(',')
            agents_so_far += str(
                list(best_agent_for_map(map_agent_graph, choice2, teammate_agents, choice1).keys()))
        return agents_so_far + '. This is ordered in descending suitable score of agents on this map'
    else:
        return ("Please input the agents your teammates are playing. Answer in the form: (Agent1),(Agent2),...,(Agent4)"
                "\n. Don't type anything if you can choose any character.")


@callback(
    Output('output-container-button2_1', 'children'),
    [Input('choice2_1', 'value'),
     Input('button2_1', 'n_clicks')],
    State('input_agent_1', 'value'),
    prevent_initial_call=True)
def update_output(choice2, button, input):
    button_clicked = ctx.triggered_id
    if button_clicked == 'button2_1':
        if choice2 == 'all':
            return "Please pick a specific map"
        if input is None:
            return "Please input an agent name."
        else:
            agent_score = map_agent_graph.get_weight(input, choice2)
            list_of_agents = compatible_agents(map_agent_graph, input)
            return ('The agent ' + str(input) + ' has a suitability score of ' + str(agent_score) + ' on the map '
                    + str(choice2) + '. And the most played agents with ' + str(input) + ' includes: '
                    + str(list(list_of_agents.keys())) + ' which is in order of descending compatibility')
    else:
        return "Enter an agent you're playing and press submit."


@callback(
    Output('text_eco', 'children'),
    Input('choice2_2', 'value'),
    prevent_initial_call=True)
def update_output(choice2):
    return eco_tree.best_buy_for_map(choice2) + ' on ' + choice2


@callback(
    Output('text_ct', 'children'),
    Input('choice2_3', 'value'),
    prevent_initial_call=True)
def update_output(choice2):
    return choice2 + ' ' + vct_tree.best_side_for_map(choice2)


# ---------------------------------------------- which agent to play ------------------------------------------------ #


if __name__ == '__main__':
    app.run(debug=False, port=8052)
