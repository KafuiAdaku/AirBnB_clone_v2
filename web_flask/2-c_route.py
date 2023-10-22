#!/usr/bin/python3
"""a script that starts a Flask web application
    route: /c/<text>: display “C ” followed by the value of the text 
    variable (replace underscore _ symbols with a space )
    Your web application must be listening on `0.0.0.0`, port `5000`"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """A function that defines what happens when the root is queried"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """A function that defines what happens when `/hbnb` is queried"""
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """A function that defines what happens when `/c/<text>` is queried"""
    mod_txt = text.replace("_", " ")
    return "C {}".format(mod_txt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
