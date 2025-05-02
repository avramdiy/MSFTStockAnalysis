from flask import Flask, render_template_string, Response
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import io
import os

app = Flask(__name__)

# Filepath
FILEPATH = r"C:\Users\avram\OneDrive\Desktop\TRG Week 22\msft.us.txt"

# HTML Template
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>MSFT Data</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css">
</head>
<body class="container">
    <h1 class="my-4">MSFT Stock Data</h1>
    {{ table | safe }}
</body>
</html>
"""

# Load and clean the data
try:
    df = pd.read_csv(FILEPATH)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    if 'OpenInt' in df.columns:
        df = df.drop(columns=['OpenInt'])
    
    # Filter for the years 2007 and 2017
    df = df[df['Date'].dt.year.isin([2007, 2017])]
except Exception as e:
    print(f"Error processing the file: {e}")
    df = pd.DataFrame()  # Empty DataFrame to avoid breaking the app

@app.route('/')
def display_file():
    if df.empty:
        return "No data available to display."
    
    # Convert the DataFrame to an HTML table
    table_html = df.to_html(classes="table table-striped table-bordered", index=False)
    
    # Render the table in the HTML template
    return render_template_string(HTML_TEMPLATE, table=table_html)


@app.route('/plot_2017')
def plot_2017():
    # Filter data for 2017
    df_2017 = df[(df['Date'].dt.year == 2017)]

    # Create a common range of months (January to December)
    months_range = pd.date_range(start="2017-01-01", end="2017-12-31", freq='M').strftime('%Y-%m')

    # Aggregate monthly low and high prices for 2017
    df_2017['Month'] = df_2017['Date'].dt.to_period('M').astype(str)
    monthly_agg_2017 = (
        df_2017.groupby('Month')
        .agg({'Low': 'mean', 'High': 'mean'})
        .reindex(months_range)
        .fillna(0)  # Fill missing values with 0 to ensure they show on the plot
    )

    # Plot the data for 2017
    plt.figure(figsize=(12, 8))
    
    # Plot the monthly low prices for 2017 (solid green)
    plt.plot(
        monthly_agg_2017.index,
        monthly_agg_2017['Low'],
        color='green',
        linestyle='-',
        marker='o',
        label='2017 Low Prices'
    )
    
    # Plot the monthly high prices for 2017 (solid red)
    plt.plot(
        monthly_agg_2017.index,
        monthly_agg_2017['High'],
        color='red',
        linestyle='-',
        marker='o',
        label='2017 High Prices'
    )

    # Chart details
    plt.title("Monthly Aggregate Low and High Prices for 2017", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.xticks(ticks=range(len(months_range)), labels=months_range, rotation=45)
    plt.legend(fontsize=12)

    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Serve the plot as a response
    return Response(buf, mimetype='image/png')


@app.route('/plot_2007')
def plot_2007():
    # Filter data for 2007
    df_2007 = df[(df['Date'].dt.year == 2007)]

    # Create a common range of months (January to December)
    months_range = pd.date_range(start="2007-01-01", end="2007-12-31", freq='M').strftime('%Y-%m')

    # Aggregate monthly low and high prices for 2007
    df_2007['Month'] = df_2007['Date'].dt.to_period('M').astype(str)
    monthly_agg_2007 = (
        df_2007.groupby('Month')
        .agg({'Low': 'mean', 'High': 'mean'})
        .reindex(months_range)
        .fillna(0)  # Fill missing values with 0 to ensure they show on the plot
    )

    # Plot the data for 2007
    plt.figure(figsize=(12, 8))
    
    # Plot the monthly low prices for 2007 (dashed green)
    plt.plot(
        monthly_agg_2007.index,
        monthly_agg_2007['Low'],
        color='green',
        linestyle='--',
        marker='x',
        label='2007 Low Prices'
    )
    
    # Plot the monthly high prices for 2007 (dashed red)
    plt.plot(
        monthly_agg_2007.index,
        monthly_agg_2007['High'],
        color='red',
        linestyle='--',
        marker='x',
        label='2007 High Prices'
    )

    # Chart details
    plt.title("Monthly Aggregate Low and High Prices for 2007", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.xticks(ticks=range(len(months_range)), labels=months_range, rotation=45)
    plt.legend(fontsize=12)

    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Serve the plot as a response
    return Response(buf, mimetype='image/png')

@app.route('/plot_2027')
def plot_2027():
    # Filter data for 2007 and 2017
    df_2007 = df[(df['Date'].dt.year == 2007)]
    df_2017 = df[(df['Date'].dt.year == 2017)]

    # Create a common range of months (January to December)
    months_range = pd.date_range(start="2007-01-01", end="2007-12-31", freq='M').strftime('%Y-%m')

    # Aggregate monthly low and high prices for 2007
    df_2007['Month'] = df_2007['Date'].dt.to_period('M').astype(str)
    monthly_agg_2007 = (
        df_2007.groupby('Month')
        .agg({'Low': 'mean', 'High': 'mean'})
        .reindex(months_range)
        .fillna(0)  # Fill missing values with 0 to ensure they show on the plot
    )

    # Aggregate monthly low and high prices for 2017
    df_2017['Month'] = df_2017['Date'].dt.to_period('M').astype(str)
    monthly_agg_2017 = (
        df_2017.groupby('Month')
        .agg({'Low': 'mean', 'High': 'mean'})
        .reindex(months_range)
        .fillna(0)  # Fill missing values with 0 to ensure they show on the plot
    )

    # Calculate the median price for each month as the average of High and Low prices
    median_2007 = (monthly_agg_2007['Low'] + monthly_agg_2007['High']) / 2
    median_2017 = (monthly_agg_2017['Low'] + monthly_agg_2017['High']) / 2

    # Prepare data for linear regression: months as a numerical value (0-11)
    months_numeric = np.arange(12).reshape(-1, 1)

    # Train a linear regression model using the 2007 and 2017 data
    model = LinearRegression()

    # Reshape median prices into a column vector for fitting the model
    median_prices = np.concatenate([median_2007.values, median_2017.values], axis=0)
    months_combined = np.concatenate([months_numeric, months_numeric + 12], axis=0)

    model.fit(months_combined, median_prices)

    # Predict the median price for 2027 (use months 0-11 for 2027)
    months_2027 = np.arange(24, 36).reshape(-1, 1)  # Months for 2027
    predicted_median_2027 = model.predict(months_2027)

    # Plot the data for the predicted median price in 2027
    plt.figure(figsize=(12, 8))
    
    # Plot the predicted median prices for 2027 (dashed blue)
    plt.plot(
        pd.date_range(start="2027-01-01", end="2027-12-31", freq='M').strftime('%Y-%m'),
        predicted_median_2027,
        color='blue',
        linestyle='--',
        marker='o',
        label='Predicted Median Prices for 2027'
    )

    # Chart details
    plt.title("Predicted Monthly Median Prices for 2027", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.xticks(ticks=range(12), labels=months_range, rotation=45)
    plt.legend(fontsize=12)

    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Serve the plot as a response
    return Response(buf, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
