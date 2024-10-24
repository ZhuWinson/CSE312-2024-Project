from flask import Flask, render_template, request, redirect
from util.accounts import register, login, logout, accountCollection
import secrets

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login_submit():
    username = request.form.get("username")
    password = request.form.get("password")
    return login(username, password)

@app.route("/login", methods=["GET"])
def login_page():
    return render_index("Login", "login_form")

@app.route("/logout", methods=["GET", "POST"])
def logout_submit():
    return logout()

@app.route("/register", methods=["POST"])
def register_submit():
    username = request.form.get("username")
    password = request.form.get("password")
    verification = request.form.get("verify")
    return register(username, password, verification)

@app.route("/register", methods=["GET"])
def register_page():
    return render_index("Registration", "register_form")

def render_index(header_title, content_type):
    username = "Guest"
    authenticated = False
    if "token" in request.cookies:
        token = request.cookies.get("token")
        authenticated = "token" in request.cookies
        user = accountCollection.find_one({"token": token})
        userContent = dict(user)
        username = userContent.get("username")

    return render_template(
        "index.html",
        authenticated=authenticated, 
        header_title=header_title,
        username=username,
        content_type=content_type)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)