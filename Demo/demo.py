# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from alliance_members import alliance_members

import base64
wordcloud_path = 'wordcloud.png'

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

        dcc.Tab(label = 'sadas', children = [
            html.Img(id = 'wordcloud'),
            dcc.Slider(
                id = 'slider-day',
                min = 1,
                max = 30,
                step = 1,
                value = 1,
                marks = {str(v): str(v) for v in range(1, 31)}
            )
        ]),
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
            height = 800,
            xaxis = {'title': xtitle, 'showgrid': True},
            yaxis = {'title': ytitle, 'showgrid': True},
            margin = {'l': 80, 'b': 40, 't': 10, 'r': 10},
            hovermode = 'closest'
        )
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
        print(a)
        length = len(a[day])
        if length != 0:
            members_of_alliances[a] = length

    print(members_of_alliances)
    wc = WordCloud(background_color = "white", width = 1000, height = 1000, relative_scaling = 0.5, normalize_plurals = False).generate_from_frequencies(members_of_alliances)
    plt.savefig('wordcloud.png')

    print('current image_path = {}'.format(wordcloud_path))
    encoded_image = base64.b64encode(open(wordcloud_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

if __name__ == '__main__':
    app.run_server(debug = True)