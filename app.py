import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Bettenbelegung in DE'


def zahl2land(b):
    c = "{0:02d}".format(b)
    a = str(c)
    zahl2landdic = {'00': 'Deutschland',
                    '01': 'Schleswig-Holstein',
                    '02': 'Freie und Hansestadt Hamburg',
                    '03': 'Niedersachsen',
                    '04': 'Freie Hansestadt Bremen',
                    '05': 'Nordrhein-Westfalen',
                    '06': 'Hessen',
                    '07': 'Rheinland-Pfalz',
                    '08': 'Baden-Württemberg',
                    '09': 'Freistaat Bayern',
                    '10': 'Saarland',
                    '11': 'Berlin',
                    '12': 'Brandenburg',
                    '13': 'Mecklenburg-Vorpommern',
                    '14': 'Freistaat Sachsen',
                    '15': 'Sachsen-Anhalt',
                    '16': 'Freistaat Thüringen'
    }
    # land2zahldic = {v: k for k, v in zahl2landdic.items()}
    return zahl2landdic[a]


s = pd.read_csv('helper/kreise.csv')
t = pd.read_csv('helper/alles.csv')


def zahl2kreis(a):
    return str(s[s['5stellig'] == a]['Gemeinden'].iat[0])


def gemeinde2zahl(string):
    return int(t[t['Gemeinde+Bundesland'] == string]['5stellig'].iat[0])


def give_cases(a, df):
    a = int(a)
    if a == 0:
        return df.groupby(['daten_stand']).sum().reset_index()
    if a < 17:
        df = df[df['bundesland'] == a].groupby(['daten_stand']).sum().reset_index()
        return df
    if a > 17:
        return df[df['gemeindeschluessel'] == a]


# import of Data
df = pd.read_csv('data/gesamt.csv', parse_dates=['daten_stand'])

stand = df['daten_stand'].max().strftime('%d.%m.%Y %H:%M')

available_indicators = np.insert(df['bundesland'].unique(), 0, 0)
available_kreise = np.array(s['5stellig'])
available_gemeinden = np.array(t['Gemeinde+Bundesland'])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H2('COVID19: Intensivbettenbelegung in Deutschland'),
    html.H3('nicht mehr aktualisiert'),
    html.Div([
        html.Div([
            html.Div([],className='one column'),
            html.Div([
                html.Label('wähle Region:'),
                dcc.Dropdown(id='demo-dropdown', options=[{'label': zahl2land(i), 'value': i} for i in available_indicators], value=0),
                html.Br(),
            ], className='four columns'),
        html.Div([
            html.Label(['oder ', html.A('Stadt/Gemeinde*:', href='https://www.riserid.eu/data/user_upload/downloads/info-pdf.s/Diverses/Liste-Amtlicher-Gemeindeschluessel-AGS-2015.pdf', target="_blank", rel="noopener noreferrer")]),
            dcc.Dropdown(id='my-input',options=[{'label': i, 'value': gemeinde2zahl(i)} for i in available_gemeinden],value=''),
         #   dcc.Input(id='my-input',placeholder='Gemeindeschlüssel',type='text',value=''),
            html.Br(),
        ], className='four columns'),
            html.Div([], className='one column'),
            html.Br(),
    ],
    className='twelve columns'),
    html.Div([
        dcc.Graph(id='my-graph')
        ],className='twelve columns'),
    html.Br(),
    html.A('Code gibt\'s hier', href='https://github.com/gnzng/covid-betten',target="_blank", rel="noopener noreferrer"),
    html.Br(),
    html.Label([html.A('Daten hier', href='https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table',target="_blank", rel="noopener noreferrer"),' | Stand: {}'.format(stand)]),
    html.Div(id='gemeinden-output',style={'color': 'grey', 'fontSize': 11}),
    html.Br(),
    html.A('Daten nicht mehr aktuell, da direktes Dashboard von DIVI vorhanden', href='https://www.intensivregister.de/#/aktuelle-lage/zeitreihen',target="_blank", rel="noopener noreferrer"),
    html.Div('Angaben sind ohne Gewähr',style={'color': 'grey', 'fontSize': 9})
])])


@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('my-input', 'value'),dash.dependencies.Input('demo-dropdown', 'value')])
def update_graph(value0,value1):
    if value0 == '':
        value = value1
    else:
        value = value0
    dff =  give_cases(value,df)

    trace1 = go.Scatter(
        x = dff['daten_stand'],
        y = dff['betten_frei'],
        name = 'Betten frei'
        )

    trace2 = go.Scatter(
        x = dff['daten_stand'],
        y = dff['betten_belegt'],
        name = 'Betten belegt'
        )

    trace3 = go.Scatter(
        x = dff['daten_stand'],
        y = dff['faelle_covid_aktuell'],
        name = 'stationär belegt wg. COVID'
        )

    trace4 = go.Scatter(
        x = dff['daten_stand'],
        y = dff['faelle_covid_aktuell_beatmet'],
        name = 'stationär beatmet wg. COVID'
        )

    data = [trace1,trace2,trace3,trace4]

    layout = go.Layout(
            xaxis = dict(title = 'Datum'), 
            yaxis = dict(title = 'Anzahl'), 
            margin = {'l': 30, 'r': 0, 't': 10, 'b': 20},
            xaxis_rangeslider_visible=True
    )
    
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        showlegend=True,
        legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=0.5
    )
    )
    return fig

@app.callback(
    dash.dependencies.Output('gemeinden-output', 'children'),
    [dash.dependencies.Input('my-input', 'value')]
)
def update_output(input_value):
    if input_value != '':
        return '* beinhaltet Gemeinden: {}'.format(zahl2kreis(input_value))

#server = app.server

if __name__ == '__main__':
    app.run_server()
