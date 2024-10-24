from flask import Flask, render_template, request
from util.accounts import register, login, logout

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home_page():
    return render_index("Trending", "post_list")

@app.route("/invalid")
def invalid():
    return "<p> Something broke </p>"

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
    return register(username, password)

@app.route("/register", methods=["GET"])
def register_page():
    return render_index("Registration", "register_form")

def render_index(header_title, content_type):
    authenticated = "token" in request.cookies
    return render_template(
        "index.html",
        authenticated=authenticated, 
        header_title=header_title,
        content_type=content_type)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)