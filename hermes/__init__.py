from flask import Flask

app = Flask(__name__)

@app.route("/")
def its_alive():
    return "<h1>It's alive</h1>"
