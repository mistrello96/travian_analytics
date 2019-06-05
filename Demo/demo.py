# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
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
        dcc.Tab(label = 'Activities over the days', children=[

            html.Div(
                dcc.Graph(
                    id = 'actvs_over_days',
                    figure = {
                        'data': [
                            go.Scatter(
                                x = activities[k]['day'],
                                y = activities[k]['nodes'],
                                text = ["Day {}".format(d) for d in activities[k]['day']],
                                mode='lines+markers',
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
                            xaxis = {'title': "Day"},
                            yaxis = {'title': "Number"},
                            margin={'l': 50, 'b': 40, 't': 45, 'r': 10},
                            legend={'x': 0.95, 'y': 0.95},
                        )
                    }
                )
            ),
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug = True)