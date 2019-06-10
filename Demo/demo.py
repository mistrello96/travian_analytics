# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from alliance_members import alliance_members

import base64
wordcloud_path = 'wordcloud.png'

large_alliances = {}
for a in alliance_members:
    for s in alliance_members[a]:
        if len(s) > 49:
            large_alliances[a] = [len(x) for x in alliance_members[a]]
            break

df_attacks_activity = pd.read_csv("../Results/Activity/attacks_activity.csv")
df_messages_activity = pd.read_csv("../Results/Activity/messages_activity.csv")
df_trades_activity = pd.read_csv("../Results/Activity/trades_activity.csv")
activities = {'Attacks': df_attacks_activity, 'Messages': df_messages_activity, 'Trades': df_trades_activity}

df_days = pd.read_csv("../Results/Activity/activity_per_hour.csv")
df_christmas = pd.read_csv("../Results/Christmas/day25_activity_per_hour.csv")
df_days.columns = df_days.columns.map(lambda x: str(x) + '_days' if x != "hour" else "hour")
df_christmas.columns = df_christmas.columns.map(lambda x: str(x) + '_christmas' if x != "hour" else "hour")
df_day_christmas = df_days.merge(df_christmas, how = "outer", on = "hour")
df_day_christmas.fillna(0)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.title = 'Travian Demo'

app.layout = html.Div(children = [
    html.H1(children = 'Travian Network'),
    dcc.Tabs(id = 'tabs', children = [
        dcc.Tab(label = 'Activities over the days', children = [
            html.Div([
                dcc.Graph(
                    id = 'players_over_days',
                    figure = {
                        'data': [
                            go.Scatter(
                                x = activities[k]['day'],
                                y = activities[k]['nodes'],
                                text = ["Day {}".format(d) for d in activities[k]['day']],
                                mode ='lines+markers',
                                opacity = 0.7,
                                marker = {
                                    'color': "red" if k == 'Attacks' else "blue" if k == "Messages" else "green",
                                    'size': 15,
                                    'line': {'width': 0.5, 'color': "red" if k == 'Attacks' else "blue" if k == "Messages" else "green"}
                                },
                                name = k
                            ) for k in activities
                        ],
                        'layout': go.Layout(
                            title = "Players over the days",
                            font = {'size': 14},
                            xaxis = {'title': "Day", 'showgrid': True, 'showline': True},
                            yaxis = {'title': "Number", 'showgrid': True},
                            margin={'l': 80, 'b': 40, 't': 45, 'r': 10},
                            legend={'x': 0.95, 'y': 0.95},
                        )
                    }
                ),
                dcc.Graph(
                    id = 'actvs_over_days',
                    figure = {
                        'data': [
                            go.Scatter(
                                x = activities[k]['day'],
                                y = activities[k]['edges'],
                                text = ["Day {}".format(d) for d in activities[k]['day']],
                                mode ='lines+markers',
                                opacity = 0.7,
                                marker = {
                                    'color': "red" if k == 'Attacks' else "blue" if k == "Messages" else "green",
                                    'size': 15,
                                    'line': {'width': 0.5, 'color': "red" if k == 'Attacks' else "blue" if k == "Messages" else "green"}
                                },
                                name = k
                            ) for k in activities
                        ],
                        'layout': go.Layout(
                            title = "Activities over the days",
                            font = {'size': 14},
                            xaxis = {'title': "Day", 'showgrid': True, 'showline': True},
                            yaxis = {'title': "Number", 'showgrid': True},
                            margin={'l': 80, 'b': 40, 't': 45, 'r': 10},
                            legend={'x': 0.95, 'y': 0.95},
                        )
                    }
               )
            ]),
            html.Div([
                html.Div([
                    html.Div([
                        html.Label('Select a day to see the respective distribution of the players performing an activity:'),
                        dcc.Dropdown(
                            id = 'dropdown-day-players',
                            options = [{'label': d, 'value': d} for d in range(1, 31)],
                            value = 1,
                        ),
                    ]),
                    html.Div([
                        dcc.Graph(id = 'pie-activities-players')
                    ]),
                ], className = "six columns"),

                html.Div([
                    html.Div([
                        html.Label('Select a day to see the respective distribution of the activities:'),
                        dcc.Dropdown(
                            id = 'dropdown-day-actions',
                            options = [{'label': d, 'value': d} for d in range(1, 31)],
                            value = 1,
                        ),
                    ]),
                    html.Div([
                        dcc.Graph(id = 'pie-activities-actions')
                    ])
                ], className = "six columns")
            ], className = "row")
        ]),


        dcc.Tab(label = 'Distribution of centralities - Aggregate graph', children = [
            html.Div([
                html.Div([
                    html.Label('Centralities:'),
                    dcc.RadioItems(
                        id = 'centrality-histogram-radio',
                        options = [
                            {'label': 'attacks received', 'value': 'attacks in-degree'},
                            {'label': 'attacks performed', 'value': 'attacks out-degree'},
                            {'label': 'attacks received and performed', 'value': 'attacks edge-count'},
                            {'label': 'messages received', 'value': 'messages in-degree'},
                            {'label': 'messages sent', 'value': 'messages out-degree'},
                            {'label': 'messages received and sent', 'value': 'messages edge-count'},
                            {'label': 'messages PageRank', 'value': 'messages PageRank'},
                            {'label': 'messages betweenness', 'value': 'messages betweenness'},
                            {'label': 'trades received', 'value': 'trades in-degree'},
                            {'label': 'trades sent', 'value': 'trades out-degree'},
                            {'label': 'trades received and sent', 'value': 'trades edge-count'},
                            {'label': 'trades PageRank', 'value': 'trades PageRank'},
                            {'label': 'trades betweenness', 'value': 'trades betweenness'}
                        ],
                        value = 'attacks in-degree'
                    ),
                    daq.ToggleSwitch(
                        id = 'switch-outliers-histogram',
                        label = ['Turn on to ignore outliers'],
                        labelPosition = 'top',
                        value = False
                    ),
                ], className = "two columns"),
                html.Div([dcc.Graph(id = 'histogram-centralities')], className = "two columns"),
            ], className = "row"),
        ]),

        dcc.Tab(label = 'Centralities jointplot - Aggregate graph', children = [
            html.Div([
                html.Div([dcc.Graph(id = 'jointplot-aggregate')], className="six columns"),
                html.Div([
                    html.Label('X axis:'),
                    dcc.RadioItems(
                        id = 'agg-x',
                        options = [
                            {'label': 'attacks received', 'value': 'attacks in-degree'},
                            {'label': 'attacks performed', 'value': 'attacks out-degree'},
                            {'label': 'messages received', 'value': 'messages in-degree'},
                            {'label': 'messages sent', 'value': 'messages out-degree'},
                            {'label': 'messages PageRank', 'value': 'messages PageRank'},
                            {'label': 'messages betweenness', 'value': 'messages betweenness'},
                            {'label': 'trades received', 'value': 'trades in-degree'},
                            {'label': 'trades sent', 'value': 'trades out-degree'},
                            {'label': 'trades PageRank', 'value': 'trades PageRank'},
                            {'label': 'trades betweenness', 'value': 'trades betweenness'}
                        ],
                        value = 'attacks in-degree'
                    ),
                    html.Label('Y axis:'),
                    dcc.RadioItems(
                        id = 'agg-y',
                        options = [
                            {'label': 'attacks received', 'value': 'attacks in-degree'},
                            {'label': 'attacks performed', 'value': 'attacks out-degree'},
                            {'label': 'messages received', 'value': 'messages in-degree'},
                            {'label': 'messages sent', 'value': 'messages out-degree'},
                            {'label': 'messages PageRank', 'value': 'messages PageRank'},
                            {'label': 'messages betweenness', 'value': 'messages betweenness'},
                            {'label': 'trades received', 'value': 'trades in-degree'},
                            {'label': 'trades sent', 'value': 'trades out-degree'},
                            {'label': 'trades PageRank', 'value': 'trades PageRank'},
                            {'label': 'trades betweenness', 'value': 'trades betweenness'}
                        ],
                        value = 'attacks out-degree'
                    ),
                    html.Label('Outliers to not be considered:'),
                    dcc.Checklist(
                        id = 'outliers',
                        options=[
                            {'label': 'attacks received', 'value': 'attacks in-degree'},
                            {'label': 'attacks performed', 'value': 'attacks out-degree'},
                            {'label': 'messages received', 'value': 'messages in-degree'},
                            {'label': 'messages sent', 'value': 'messages out-degree'},
                            {'label': 'trades received', 'value': 'trades in-degree'},
                            {'label': 'trades sent', 'value': 'trades out-degree'}
                        ],
                        values = []
                    ),
                    html.Button('Select all', id = 'select-all-outliers')
                ], className = "six columns"),
            ], className = "row"),
        ]),

        dcc.Tab(label = "Number of alliances' members", children = [
            html.Div([
                html.Div([html.Img(id = 'wordcloud')], className = "four columns"),
                html.Div([
                    html.Label('Select communities:'),
                    dcc.Dropdown(
                        id = 'dropdown-communities',
                        options = [{'label': a, 'value': a} for a in large_alliances],
                        value = ['alliance43'],
                        style = {'width': 1250},
                        multi = True
                    ),
                    dcc.Graph(id = 'communities-evolution-graph'),
                ], className = "six columns"),
            ], className = "row"),
            html.Label('Select a day:'),
            dcc.Slider(
                id = 'slider-day',
                min = 1,
                max = 30,
                step = 1,
                value = 1,
                marks = {str(v): str(v) for v in range(1, 31)}
            )
        ]),

        dcc.Tab(label = "Analysis of Christmas", children = [
            dcc.Graph(
                id = 'christmas-activities',
                figure = {
                    'data': [
                        go.Scatter(
                            x = df_day_christmas["hour"],
                            y = [x / 30 for x in df_day_christmas[k]] if k == "attacks_days" or k == "messages_days" or k == "trades_days" else df_day_christmas[k],
                            text = ["h: {}.00".format(h) for h in df_days["hour"]],
                            mode ='lines+markers',
                            opacity = 0.7,
                            marker = {
                                'color': "red" if k == 'attacks' else "blue" if k == "messages" else "green",
                                'size': 15,
                                'line': {'width': 0.5, 'color': "red" if k == 'attacks' else "blue" if k == "messages" else "green"} if k.split('_')[1] == "days" 
                                        else {'width': 0.5, 'color': "red" if k == 'attacks' else "blue" if k == "messages" else "green"}
                            },
                            name = "{} average".format(k.split('_')[0][0].upper()+ k.split('_')[0][1:]) if k.split('_')[1] == "days" 
                                        else "{} on Christmas".format(k.split('_')[0][0].upper()+ k.split('_')[0][1:])
                        ) for k in ["attacks_days", "messages_days", "trades_days", "attacks_christmas", "messages_christmas", "trades_christmas"]
                    ],
                    'layout': go.Layout(
                        title = "Players over the days",
                        font = {'size': 14},
                        xaxis = {'title': "Day", 'showgrid': True, 'showline': True},
                        yaxis = {'title': "Number", 'showgrid': True},
                        margin={'l': 80, 'b': 40, 't': 45, 'r': 10},
                        legend={'x': 0.95, 'y': 0.95},
                    )
                }
            ),
        ])
    ])
])

@app.callback(
    Output('jointplot-aggregate', 'figure'),
    [Input('agg-x', 'value'),
     Input('agg-y', 'value'),
     Input('outliers', 'values')])
def update_aggregate_joinplot(x, y, outliers):
    x = x.split()
    y = y.split()

    dfx = pd.read_csv("../Results/Aggregate/{}_{}.csv".format(x[0], 
        'degree' if x[1] == 'in-degree' or x[1] == 'out-degree' else 'centrality'))
    
    dfy = pd.read_csv("../Results/Aggregate/{}_{}.csv".format(y[0], 
        'degree' if y[1] == 'in-degree' or y[1] == 'out-degree' else 'centrality'))
    
    dfx.columns = dfx.columns.map(lambda x: str(x) + '_x' if x != "node" else "node")
    dfy.columns = dfy.columns.map(lambda x: str(x) + '_y' if x != "node" else "node")
    df = dfx.merge(dfy, how = "outer", on = "node")
    df.fillna(0)

    outliers_lims = {'attacks in-degree': 950,
                     'attacks out-degree': 3749,
                     'messages in-degree': 693,
                     'messages out-degree': 1608,
                     'trades in-degree': 732,
                     'trades out-degree': 693}

    for o in outliers:
        (edge_type, degree_type) = o.split()
        if edge_type == x[0] or edge_type == y[0]:
            df_tmp = pd.read_csv("../Results/Aggregate/{}_degree.csv".format(edge_type))
            outliers_nodes = df_tmp[df_tmp[degree_type] > outliers_lims[o]]["node"]
            df.drop(df[df["node"].isin(outliers_nodes)].index, inplace = True)


    colors = {'attacks-attacks': "red",
              'attacks-messages': "purple",
              'attacks-trades': "brown",
              'messages-attacks': "purple",
              'messages-messages': "blue",
              'messages-trades': "orange",
              'trades-attacks': "brown",
              'trades-messages': "orange",
              'trades-trades': "green"}

    xtitle = "{} {}".format(x[0][0].upper() + x[0][1:], x[1][0].upper() + x[1][1:])
    ytitle = "{} {}".format(y[0][0].upper() + y[0][1:], y[1][0].upper() + y[1][1:])

    xs = "{}_x".format(x[1])
    ys = "{}_y".format(y[1])

    traces = go.Scatter(x = df[xs], y = df[ys],
        text = ["id: {} x: {}  y: {}".format(id_node, round(xv, 5), round(yv, 5)) for id_node, xv, yv in zip(df["node"], df[xs], df[ys])],
        mode = 'markers', opacity = 0.7, marker = { 'color': colors["{}-{}".format(x[0], y[0])], 'size': 10},
        hoverinfo = 'text'
    )

    return {
        'data': [traces],
        'layout': go.Layout(
            font = {'size': 14},
            autosize = False,
            width = 800,
            height = 750,
            xaxis = {'title': xtitle, 'showgrid': True},
            yaxis = {'title': ytitle, 'showgrid': True},
            margin = {'l': 80, 'b': 40, 't': 10, 'r': 10},
            hovermode = 'closest'
        )
    }

@app.callback(
    Output('pie-activities-players', 'figure'),
    [Input('dropdown-day-players', 'value')])
def update_pie_activities_players(day):
    labels = []
    values = []
    for activity in activities:
        labels.append(activity)
        values.append(activities[activity]['nodes'][day - 1])
    colors = ['red', 'blue', 'green']
    trace = go.Pie(labels = labels, values = values, hoverinfo = 'label+percent',
                   textinfo = 'value', textfont = dict(size = 20), marker = dict(colors = colors, line = dict(color = '#000000', width = 2)))
    return{
        'data': [trace],
        'layout': {'height': 250, 'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10}}
    }

@app.callback(
    Output('pie-activities-actions', 'figure'),
    [Input('dropdown-day-actions', 'value')])
def update_pie_activities_actions(day):
    labels = []
    values = []
    for activity in activities:
        labels.append(activity)
        values.append(activities[activity]['edges'][day - 1])
    colors = ['red', 'blue', 'green']
    trace = go.Pie(labels = labels, values = values, hoverinfo = 'label+percent',
                   textinfo = 'value', textfont = dict(size = 20), marker = dict(colors = colors, line = dict(color = '#000000', width = 2)))
    return{
        'data': [trace],
        'layout': {'height': 250, 'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10}}
    }

@app.callback(
    Output('histogram-centralities', 'figure'),
    [Input('centrality-histogram-radio', 'value'),
     Input('switch-outliers-histogram', 'value')])
def update_histogram(centrality, outliers):
    x = centrality.split()
    df = pd.read_csv("../Results/Aggregate/{}_{}.csv".format(x[0],
                     'degree' if x[1] == 'in-degree' or x[1] == 'out-degree' or x[1] == 'edge-count' else 'centrality'))

    outliers_lims = {'attacks in-degree': 950,
                     'attacks out-degree': 3749,
                     'attacks edge-count': 3803,
                     'messages in-degree': 693,
                     'messages out-degree': 1608,
                     'messages edge-count': 2246,
                     'trades in-degree': 732,
                     'trades out-degree': 693,
                     'trades edge-count': 1392}

    if outliers:
        df_tmp = pd.read_csv("../Results/Aggregate/{}_degree.csv".format(x[0]))
        outliers_nodes = df_tmp[df_tmp["in-degree"] > outliers_lims["{} in-degree".format(x[0])]]["node"]
        df.drop(df[df["node"].isin(outliers_nodes)].index, inplace = True)         
        outliers_nodes = df_tmp[df_tmp["out-degree"] > outliers_lims["{} out-degree".format(x[0])]]["node"]
        df.drop(df[df["node"].isin(outliers_nodes)].index, inplace = True)         
        outliers_nodes = df_tmp[df_tmp["edge-count"] > outliers_lims["{} edge-count".format(x[0])]]["node"]
        df.drop(df[df["node"].isin(outliers_nodes)].index, inplace = True)         
    trace = go.Histogram(x = df[x[1]], histnorm = 'probability', opacity = 0.7,
                         marker = dict(color = 'red' if x[0] == 'attacks' else 'blue' if x[0] == 'messages' else 'green'))
    xtitle = "{} {}".format(x[0][0].upper() + x[0][1:], x[1][0].upper() + x[1][1:])
    
    return {
        'data': [trace],
        'layout': go.Layout(
            autosize = False,
            width = 1550,
            height = 600,
            xaxis = {'title': xtitle},
            yaxis = {"type": "log", 'title': "Probability"},
            margin = {'l': 80, 'b': 40, 't': 10, 'r': 10},)
    }

@app.callback(
    Output('outliers', 'values'),
    [Input('select-all-outliers', 'n_clicks')],
    [State('outliers', 'options'),
     State('outliers', 'values')])
def select_all_outliers(n_clicks, options, values):
    if n_clicks != None:
        return [i['value'] for i in options]
    else: 
        return values

@app.callback(
    Output('wordcloud', 'src'),
    [Input('slider-day', 'value')])
def update_wordcloud(day):
    members_of_alliances = {}
    for a in alliance_members:
        length = len(alliance_members[a][day])
        if length != 0:
            members_of_alliances[a] = length

    wc = WordCloud(background_color = "white", width = 600, height = 600, relative_scaling = 0.5, normalize_plurals = False).generate_from_frequencies(members_of_alliances)
    wc.to_file("wordcloud.png")

    encoded_image = base64.b64encode(open(wordcloud_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

@app.callback(
    Output('communities-evolution-graph', 'figure'),
    [Input('dropdown-communities', 'value')])
def update_relevant_communities_graph(alliances_of_interest):
    traces = []
    for a in alliances_of_interest:
        traces.append(go.Scatter(x = [d for d in range(1, 31)], y = large_alliances[a],
            text = ["Day {}".format(d) for d in range(1, 31)], mode ='lines+markers',
            opacity = 0.7, marker = {'size': 15, 'line': {'width': 0.5}}, name = a))

    return {
        'data': traces,
        'layout': go.Layout(
            title = "Number of members over the days",
            font = {'size': 14},
            autosize = False,
            width = 1250,
            height = 550,
            xaxis = {'title': "Day", 'showgrid': True, 'showline': True},
            yaxis = {'title': "Number", 'showgrid': True},
            margin={'l': 80, 'b': 40, 't': 45, 'r': 10},
            legend={'x': 0.95, 'y': 0.95},
        )
    }

if __name__ == '__main__':
    app.run_server(debug = False)