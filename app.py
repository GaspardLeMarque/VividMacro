import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request
import plotly.graph_objects as go
from fredapi import Fred
import parser

# Parse an .env file
load_dotenv()
fred = Fred(api_key=os.environ.get('API_KEY'))

# Create an app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/plot', methods=['POST'])
def plot():
    if 'series_id' in request.form:
        # Handle the request from the first form
        series_id = request.form['series_id']
        series_content = fred.search(series_id).T
        fred_data = fred.get_series(series_id)
        if fred_data is None:
            return "Failed to retrieve data from the FRED API."

        # Create a Plotly figure with updated layout using API data
        fig = go.Figure(data=go.Scatter(x=fred_data.index, y=fred_data))

        fig.update_layout(
            title=series_content.loc['title'][series_id],
            xaxis=dict(title='Date'),
            yaxis=dict(title=series_content.loc['units'][series_id]),
            annotations=[
                dict(
                    text=series_content.loc['notes'][series_id],
                    x=0.5,
                    y=-0.3,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=14)
                )
            ],
            showlegend=False
        )
    elif 'column_name' in request.form:
        # Handle the request from the second form
        column_name = request.form['column_name']
        ascii_data = parser.df

        if ascii_data is None:
            return "Failed to retrieve data for the plot."

        if column_name not in ascii_data.columns:
            return "Invalid column name."

        # Create a Plotly figure with updated layout using dataframe column
        fig = go.Figure(data=go.Scatter(x=ascii_data.index, y=ascii_data[column_name]))

        fig.update_layout(
            title=column_name,
            xaxis=dict(title='Date'),
            yaxis=dict(title='Value'),
            showlegend=False
        )
    else:
        return "Invalid form submission."

    # Convert the figure to JSON for rendering in the template
    fig_json = fig.to_json()

    # Pass the figure JSON to the template for rendering
    return render_template('plot.html', fig_json=fig_json)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
