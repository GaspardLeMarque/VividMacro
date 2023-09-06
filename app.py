import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import plotly.graph_objects as go
from fredapi import Fred
import filter_ascii
import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
import statsmodels.api as sm

# Parse an .env file
load_dotenv()
fred = Fred(api_key=os.environ.get('API_KEY'))

# Create an app
app = Flask(__name__)

# Define ASCII data as a dataframe
ascii_data = filter_ascii.filtered_df


@app.route('/')
def index():
    return render_template('index.html', columns=ascii_data.columns)


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
                    text="",
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
    return render_template('plot.html', fig_json=fig_json, columns=ascii_data.columns)


def is_monthly(series_id):
    series_content = fred.search(series_id).T
    frequency = series_content.loc['frequency_short'][series_id]
    return frequency == 'M'


@app.route('/perform_var', methods=['POST'])
def perform_var():
    # Get series names from form inputs
    series1_name = request.form['series1_id']
    series2_name = request.form['series2_id']

    # Check if the series are monthly
    if not (is_monthly(series1_name) and is_monthly(series2_name)):
        return render_template('var_results.html', error_message="Only monthly series are allowed.")

    # Fetch data from FRED using series names
    variable_codes = [series1_name, series2_name]

    # Preprocess the data
    data = {}
    for code in variable_codes:
        raw_data = fred.get_series(code)
        log_diff_data = np.log(raw_data).diff().dropna()
        data[code] = log_diff_data

    # Create a common date index by finding the intersection of dates
    common_dates = set(data[variable_codes[0]].index)

    for code in variable_codes[1:]:
        common_dates.intersection_update(data[code].index)

    # Align all data to the common date index
    for code in variable_codes:
        data[code] = data[code].loc[list(sorted(common_dates))]

    # Perform VAR analysis
    model = VAR(pd.concat([data[code] for code in variable_codes], axis=1), freq='MS')
    results = model.fit()

    # Calculate and plot ACF for series1
    acf_series1 = sm.tsa.acf(results.resid[0], nlags=40)
    trace_series1 = go.Bar(x=list(range(len(acf_series1))), y=acf_series1, name=f'ACF - {series1_name}')

    # Calculate and plot ACF for series2
    acf_series2 = sm.tsa.acf(results.resid[1], nlags=40)
    trace_series2 = go.Bar(x=list(range(len(acf_series2))), y=acf_series2, name=f'ACF - {series2_name}')

    # Create a Plotly figure with the ACF plots
    fig = go.Figure(data=[trace_series1, trace_series2])
    fig.update_layout(title='ACF Plot for Residuals')

    return render_template('var_results.html', plot=fig.to_html())


# Run server
if __name__ == '__main__':
    app.run(debug=True)
