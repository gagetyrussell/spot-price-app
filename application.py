import requests
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

response = requests.get('http://api.eia.gov/category/?api_key=27d5df4fc1b5d3fd846986305ff2bd1e&category_id=241335')
rsp = response.json()
option_json = rsp['category']['childseries']
option_labels = [cat['name'] for cat in option_json]
option_values = [cat['series_id'] for cat in option_json]
dropdown_options = [{'label': label, 'value': value} for label, value in zip(option_labels, option_values)]


app = dash.Dash()
application = app.server

app.layout = html.Div([
    dcc.Dropdown(
        id='spot-price-category-dropdown',
        options=dropdown_options,
        value=dropdown_options[0]['value']
    ),
    dcc.Graph(id='dd-output-container')
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'figure'),
    [dash.dependencies.Input('spot-price-category-dropdown', 'value')])
def update_output(value):
    endpoint = f'http://api.eia.gov/series/?api_key=27d5df4fc1b5d3fd846986305ff2bd1e&series_id={value}'
    response = requests.get(endpoint)
    rsp = response.json()
    df = pd.DataFrame(rsp['series'][0]['data'], columns=['date', 'value'])
    figure=dict(
            data=[
                dict(
                y=df['value'],
                    x=df['date'],
                    name='Spot Price',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                )
            ]
        )
    return figure



if __name__ == '__main__':
    # Beanstalk expects it to be running on 8080.
    application.run(debug=True, port=8080)
