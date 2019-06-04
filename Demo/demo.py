# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

attacks_path = "./../datas_paper/Dataset/attack-gml/"
messages_path = "./../datas_paper/Dataset/messages-gml/"
trades_path = "./../datas_paper/Dataset/trade-gml/"

attacks_file = "./../datas_paper/Dataset/SG_attacks.graphml"
messages_file = "./../datas_paper/Dataset/SG_messages.graphml"
trade_file = "./../datas_paper/Dataset/SG_trades.graphml"



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'Travian Demo'
'''
app.layout = html.Div(children=[
    html.H1(children='Travian Network'),

    html.Div(children='''
        Analisi delle community principali
    '''),

    html.Div(
        dcc.Graph(
            id='day--community--graph',
            figure={
                'data': [
                    #{'x': list(stops_counts[13].keys()), 'y': list(stops_counts[13].values()), 'type': 'bar', 'name': 'SF'},
                ],
                'layout': {
                    'title': 'Grafo delle community per giorno',
                    'font': {
                        'size': 5
                    }
                }
            }
        )
    ),

    html.Div(
        dcc.Slider(
            id='day--slider--community',
            min=1,
            max=30,
            value=15,
            marks={str(i): str(i) for i in range(1,30)},
            step=None
        ),
        style = {'margin-bottom': 20, 'width': 800, 'margin-left': 300}
    )
])
'''
if __name__ == '__main__':
    app.run_server(debug=True)