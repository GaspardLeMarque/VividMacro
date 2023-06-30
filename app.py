import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import plotly.graph_objects as go
from fredapi import Fred

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
    series_id = request.form['series_id']
    data = fred.get_series(series_id)

    if data is not None:
        # Create a Plotly figure
        fig = go.Figure(data=go.Scatter(x=data.index, y=data))

        fig.update_layout(
            title=series_id,
            xaxis=dict(title='Date'),
            yaxis=dict(title='Value'),
            showlegend=False
        )

        # Convert the figure to JSON for rendering in the template
        fig_json = fig.to_json()

        # Pass the figure JSON to the template for rendering
        return render_template('plot.html', fig_json=fig_json)
    else:
        return "Failed to retrieve data from the FredAPI."


# Run server
if __name__ == '__main__':
    app.run(debug=True)
