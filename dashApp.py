
import dash
import dash_core_components as dcc
import dash_html_components as html
# from weatherDataPandas import DASH_PLOT_DATA, chosen_parameter
import getdata

data = getdata.main()

app = dash.Dash()

app.layout = html.Div(children=[
	html.H1(
		children='Weather Data Dashboard',
		style={
			'textAlign': 'center'
		}

		),

	html.Div(
		children='User selected epw data and sites',
		style={
			'textAlign': 'center'
			}
		),
	dcc.Graph(
		id='plot',
		figure={
		'data': data[0]
		,
		'layout':{
			'title': data[1] + ' comparison'
		}
		})
	])
if __name__ == '__main__':
	app.run_server(debug=False)
