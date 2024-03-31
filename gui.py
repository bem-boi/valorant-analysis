from dash import Dash, html, dcc

from graph import clean_agents_pick_file, clean_teams_picked_agents_file, load_agent_role_data, load_map_agent_data, \
    generate_weighted_graph, return_graph

import plotly.graph_objs as go


# INITIALIZE DATA
cleaned_agf_file = clean_agents_pick_file('graph_data/agents_pick_rates2023.csv')
cleaned_tpa_file = clean_teams_picked_agents_file('graph_data/teams_picked_agents2023.csv')
agent_role_data = load_agent_role_data('graph_data/agent_roles.csv')

map_agent_data = load_map_agent_data(cleaned_agf_file, cleaned_tpa_file, agent_role_data)
map_agent_graph = generate_weighted_graph(map_agent_data)

fig1 = return_graph(agent_role_data, map_agent_data)
# fig = go.fig1

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Valorant Analysis App'),
    html.Hr(),
    dcc.RadioItems(options=['Which Agents to play?', 'Eco-Round', 'C/CT-sided?'], value='Which Agents to play?'),
    dcc.Graph(figure=return_graph(agent_role_data, map_agent_data))
])

if __name__ == '__main__':
    app.run(debug=True)
