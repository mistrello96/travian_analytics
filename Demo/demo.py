# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

attacks_path = "./../datas_paper/Dataset/attack-gml/"
messages_path = "./../datas_paper/Dataset/messages-gml/"
trades_path = "./../datas_paper/Dataset/trade-gml/"

attacks_file = "./../datas_paper/Dataset/SG_attacks.graphml"
messages_file = "./../datas_paper/Dataset/SG_messages.graphml"
trade_file = "./../datas_paper/Dataset/SG_trades.graphml"

df_attacks_activity = pd.read_csv("../Results/Activity/attacks_activity.csv")
df_messages_activity = pd.read_csv("../Results/Activity/messages_activity.csv")
df_trades_activity = pd.read_csv("../Results/Activity/trades_activity.csv")
activities = {'Attacks': df_attacks_activity, 'Messages': df_messages_activity, 'Trades': df_trades_activity}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.title = 'Travian Demo'

app.layout = html.Div(children = [
    html.H1(children = 'Travian Network'),
    dcc.Tabs(id = 'tabs', children = [
        dcc.Tab(label = 'Activities over the days', children = [
            html.Div(
                dcc.Graph(
                    id = 'actvs_over_days',
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
                            title = "Activities over the days",
                            font = {'size': 14},
                            xaxis = {'title': "Day", 'showgrid': True, 'showline': True},
                            yaxis = {'title': "Number", 'showgrid': True},
                            margin={'l': 80, 'b': 40, 't': 45, 'r': 10},
                            legend={'x': 0.95, 'y': 0.95},
                        )
                    }
                )
            ),
        ]),

        dcc.Tab(label = 'Centralities jointplot in the aggregate graph', children = [
            #html.Div([dcc.Graph(id = 'jointplot-aggregate')]),
            html.Div([
                html.Div([dcc.Graph(id = 'jointplot-aggregate')], className="six columns"),
                html.Div([
                    html.Label('X axis:'),
                    dcc.RadioItems(
                        id = 'agg-x',
                        options = [
                            {'label': 'attacks received', 'value': 'attacks in-degree'},
                            {'label': 'attacks performed', 'value': 'attacks out-degree'},
                            {'label': 'attacks PageRank', 'value': 'attacks PageRank'},
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
                            {'label': 'attacks PageRank', 'value': 'attacks PageRank'},
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
                            {'label': 'attacks received', 'value': 'a-in'},
                            {'label': 'attacks performed', 'value': 'a-out'},
                            {'label': 'messages received', 'value': 'm-in'},
                            {'label': 'messages sent', 'value': 'm-out'},
                            {'label': 'trades received', 'value': 't-in'},
                            {'label': 'trades sent', 'value': 't-out'}
                        ],
                        values = []
                    ),
                ], className = "six columns"),
            ], className = "row"),
        ]),
    ])
])

@app.callback(
    Output('jointplot-aggregate', 'figure'),
    [Input('agg-x', 'value'),
     Input('agg-y', 'value')])
def update_aggregate_joinplot(x, y):
    x = x.split()
    y = y.split()

    dfx = pd.read_csv("../Results/Aggregate/{}_{}.csv".format(x[0], 
        'degree' if x[1] == 'in-degree' or x[1] == 'out-degree' else 'centrality'))
    
    dfy = pd.read_csv("../Results/Aggregate/{}_{}.csv".format(y[0], 
        'degree' if y[1] == 'in-degree' or y[1] == 'out-degree' else 'centrality'))
    
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

    traces = go.Scatter(x = dfx[x[1]], y = dfy[y[1]],
        text = ["x: {}  y: {}".format(xv, yv) for xv, yv in zip(dfx[x[1]], dfy[y[1]])],
        mode = 'markers', opacity = 0.7, marker = { 'color': colors["{}-{}".format(x[0], y[0])], 'size': 10},
        hoverinfo = 'text'
        #name = "player"
    )

    return {
        'data': [traces],
        'layout': go.Layout(
            font = {'size': 14},
            autosize = False,
            width = 800,
            height = 800,
            xaxis = {'title': xtitle, 'showgrid': True},
            yaxis = {'title': ytitle, 'showgrid': True},
            margin = {'l': 80, 'b': 40, 't': 10, 'r': 10},
            hovermode = 'closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug = True)