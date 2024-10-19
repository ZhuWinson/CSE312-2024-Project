from flask import Flask, redirect, url_for, render_template, request
from util.accounts import register, login, accountCollection

app = Flask(__name__)

# respond with "index.html" contents
@app.route("/")
def homehtml():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def registerForm():
    username = request.form.get("username")
    password = request.form.get("password")
    return register(username, password)

@app.route("/login", methods=["POST"])
def loginForm():
    username = request.form.get("username")
    password = request.form.get("password")
    return login(username, password)

@app.route("/rTest")
def rTest():
    return f"<p> Registered </p>"

@app.route("/lTest")
def lTest():
    return f"<p> Logged In </p>"

@app.route("/invalid")
def invalid():
    return "<p> Something broke </p>"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)