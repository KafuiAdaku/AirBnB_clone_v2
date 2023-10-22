#!/usr/bin/python3
"""a script that starts a Flask web application
   route: /number_odd_or_even/<n>: display a HTML page only if n is an integer:
        `H1` tag: “Number: n is even|odd” inside the tag `BODY`
    Your web application must be listening on `0.0.0.0`, port `5000`"""
from flask import Flask, render_template


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


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def py_text(text="is cool"):
    """A function that defines what happens when `/python/<text>` is queried"""
    mod_txt = text.replace("_", " ")
    return "Python {}".format(mod_txt)


@app.route('/number/<int:n>', strict_slashes=False)
def disp_number(n):
    """A function that defines what happens when `/number/<n>` is queried"""
    if isinstance(n, int):
        return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """displays a HTML page only if n is an integer"""
    if isinstance(n, int):
        return render_template("5-number.html", n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_or_even(n):
    """display a HTML page only if n is an integer"""
    if isinstance(n, int):
        return render_template("6-number_odd_or_even.html", number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
