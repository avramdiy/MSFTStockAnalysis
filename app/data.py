from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# Filepath
FILEPATH = r"C:\Users\avram\OneDrive\Desktop\TRG Week 22\msft.us.txt"

# HTML
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>File Data</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css">
</head>
<body class="container">
    <h1 class="my-4">$MSFT Data</h1>
    {{ table | safe }}
</body>
</html>
"""

@app.route('/')
def display_file():
    if not os.path.exists(FILEPATH):
        return f"File not found: {FILEPATH}"
    
    # Read the file into a DataFrame
    try:
        df = pd.read_csv(FILEPATH)
    except Exception as e:
        return f"Error reading file: {e}"
    
    # Convert the DataFrame to an HTML table
    table_html = df.to_html(classes="table table-striped table-bordered", index=False)
    
    # Render the table in the HTML template
    return render_template_string(HTML_TEMPLATE, table=table_html, filename=os.path.basename(FILEPATH))

if __name__ == "__main__":
    app.run(debug=True)
