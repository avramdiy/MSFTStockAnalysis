from flask import Flask, render_template_string
import pandas as pd
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

if __name__ == "__main__":
    app.run(debug=True)
