from datetime import datetime
import pandas as pd
import parser


def filter_data(df):
    """
    Filter the Dataframe by performing the following steps:
    1. Convert the dates into datetime objects and rename the index column to 'Date'.
    2. Filter out variables that have less than 50% of NaNs.

    Parameters:
        df (pandas.DataFrame): The input DataFrame to be filtered.

    Returns:
        pandas.DataFrame: The filtered DataFrame.

    Example:
        filtered_df = filter_data_with_observations(df)
    """
    # Convert dates into datetime objects and rename index col
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df.index = [datetime.strptime(i, '%Y-%m') for i in [i.strftime('%Y-%m') for i in df.index]]
    df.index.names = ['Date']

    # Filter out variables that have less than 50% of NaNs
    missing_percentage = (df.isna().sum() / df.shape[0]).round(2)
    result = [(idx, missing_percentage[idx]) for idx in missing_percentage.index]
    filtered_nans = list(filter(lambda x: x[1] <= 0.5, sorted(result, key=lambda x: x[1])))

    # Save filtered df
    result = df.copy()[[i[0] for i in filtered_nans]]

    return result


# Apply data filtering
filtered_df = filter_data(parser.df)
