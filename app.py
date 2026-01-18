from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Number Table</title>
    <style>
        table {
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #333;
            padding: 8px 12px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h2>Enter a Number</h2>
    <form method="POST">
        <input type="number" name="number" required>
        <button type="submit">Generate Table</button>
    </form>

    {% if number %}
        <h3>Table of {{ number }}</h3>
        <table>
            <tr>
                <th>Multiplier</th>
                <th>Result</th>
            </tr>
            {% for i, val in table %}
            <tr>
                <td>{{ i }}</td>
                <td>{{ val }}</td>
            </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    number = None
    table = []

    if request.method == "POST":
        number = int(request.form["number"])
        table = [(i, number * i) for i in range(1, 11)]

    return render_template_string(HTML, number=number, table=table)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
