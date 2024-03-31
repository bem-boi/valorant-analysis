from dash import Dash, dcc, html, Input, Output, callback, State, ctx

import graph
from graph import clean_agents_pick_file, clean_teams_picked_agents_file, load_agent_role_data, load_map_agent_data, \
    generate_weighted_graph, return_graph

import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# INITIALIZE DATA
cleaned_agf_file = clean_agents_pick_file('graph_data/agents_pick_rates2023.csv')
cleaned_tpa_file = clean_teams_picked_agents_file('graph_data/teams_picked_agents2023.csv')
agent_role_data = load_agent_role_data('graph_data/agent_roles.csv')
map_agent_data = load_map_agent_data(cleaned_agf_file, cleaned_tpa_file, agent_role_data)
map_agent_graph = generate_weighted_graph(map_agent_data)


app = Dash(__name__)

app.layout = html.Div([
    html.H1('Valorant Analysis App'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Which Agents to play', value='tab-1'),
        dcc.Tab(label='Eco-Round', value='tab-2'),
        dcc.Tab(label='C/CT-sided', value='tab-3')
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
                ['duelists',
                 'controllers',
                 'initiators',
                 'sentinels', 'all'], 'all', inline=True, id='choice1'),
            dcc.RadioItems(
                ['ascent',
                 'pearl',
                 'split',
                 'lotus',
                 'icebox',
                 'fracture',
                 'bind',
                 'haven', 'all'], 'all', inline=True, id='choice2'),
            dcc.Graph(figure={}, id='visual_graph'),
            html.Hr(),
            html.Div(dcc.Input(id='input_user', type='text')),
            html.Button('Submit', id='button'),
            html.Div(id='output-container-button',
                     children='Enter a value and press submit')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Eco-Round')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('C/CT-sided')
        ])

    html.Div(id='tabs-content')


@callback(
    Output(component_id='visual_graph', component_property='figure'),
    [Input(component_id='choice1', component_property='value'),
     Input(component_id='choice2', component_property='value')]
)
def update_graph(choice1, choice2):
    fig = return_graph(map_agent_data, choice1, choice2)
    return fig


@callback(
    Output('output-container-button', 'children'),
    [Input('choice1', 'value'),
     Input('choice2', 'value'),
     Input('button', 'n_clicks')],
    State('input_user', 'value'),
    prevent_initial_call=True)
def update_output(choice1, choice2, button, input):
    button_clicked = ctx.triggered_id
    if button_clicked == 'button':
        agents_so_far = 'The best agent to play on ' + choice2 + ' are '
        if choice1 == 'all':
            choice1 = ''
        if input is None:
            agents_so_far += str(
                list(graph.best_agent_for_map(map_agent_graph, choice2, [], choice1).keys()))
        else:
            teammate_agents = input.split(',')
            agents_so_far += str(
                list(graph.best_agent_for_map(map_agent_graph, choice2, teammate_agents, choice1).keys()))
        return agents_so_far + '. This is ordered in descending suitable score of agents on this map'
    else:
        return ("Please input the agents your teammates are playing. Answer in the form: (Agent1),(Agent2),...,(Agent4)"
                "\n. Don't type anything if you can choose any character.")


if __name__ == '__main__':
    app.run(debug=True)
