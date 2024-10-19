from flask import Flask, redirect, url_for, render_template, request
from util.accounts import register, login, logout

app = Flask(__name__)

@app.route("/")
def homehtml():
    if "token" in request.cookies:
        return render_template("loggedin.html")
    return render_template("loggedout.html")

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

@app.route("/logout", methods=["POST"])
def logoutForm():
    return logout()

@app.route("/invalid")
def invalid():
    return "<p> Something broke </p>"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)