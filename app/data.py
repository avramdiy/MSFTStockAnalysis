from flask import Flask, render_template_string, Response
import pandas as pd
import matplotlib.pyplot as plt
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
    df = df[df['Date'] >= '2000-01-01']
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

@app.route('/plot')
def plot_monthly_low_high():
    # Filter data for 2017
    df_2017 = df[(df['Date'].dt.year == 2017)]

    # Aggregate monthly low and high prices
    df_2017['Month'] = df_2017['Date'].dt.to_period('M')
    monthly_agg = df_2017.groupby('Month').agg({'Low': 'mean', 'High': 'mean'})

    # Plot the data
    plt.figure(figsize=(10, 6))
    
    # Plot the monthly low prices
    plt.plot(
        monthly_agg.index.to_timestamp(),
        monthly_agg['Low'],
        color='green',
        linestyle='-',
        marker='o',
        label='Monthly Low Prices'
    )
    
    # Plot the monthly high prices
    plt.plot(
        monthly_agg.index.to_timestamp(),
        monthly_agg['High'],
        color='red',
        linestyle='-',
        marker='o',
        label='Monthly High Prices'
    )
    
    plt.title("Monthly Aggregate Low and High Prices for 2017", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
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
