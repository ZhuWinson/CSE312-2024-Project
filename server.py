import html
import json
from flask import Flask, make_response, redirect, render_template, request
from util.accounts import register, login, logout, purge_accounts, accountCollection
from util.posts import create_post, like_post, list_posts, purge_posts
from util.renderer import render_home_page

app = Flask(__name__, static_url_path="/static")
 
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "max-age=3600"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response 

@app.route("/invalidpassword")
def invalid_password():
    return "<p> Invalid Password </p>",{"Refresh": "1; url=http://localhost:8080/"}

@app.route("/passwordmismatch")
def mismatch_password():
    return "<p> Passwords Do Not Match </p>",{"Refresh": "1; url=http://localhost:8080/"}

@app.route("/usertaken")
def user_taken():
    return "<p> Username Taken </p>",{"Refresh": "1; url=http://localhost:8080/"}

@app.route("/account", methods=["GET"])
def account_page():
    auth_token = request.cookies.get("auth_token")
    return render_home_page("Account Info", "account_info", auth_token)

@app.route("/create", methods=["POST"])
def create():
    auth_token = request.cookies.get("auth_token")
    title = html.escape(request.form.get("title", ""))
    message = html.escape(request.form.get("message", ""))
    create_post(title, message, auth_token)
    return redirect("/")

@app.route("/create", methods=["GET"])
def create_page():
    auth_token = request.cookies.get("auth_token")
    return render_home_page("Create Post", "create_form", auth_token)

@app.route("/", methods=["GET"])
def home_page():
    auth_token = request.cookies.get("auth_token")
    return render_home_page("Home", "post_list", auth_token)

@app.route("/login", methods=["POST"])
def login_submit():
    username = html.escape(request.form.get("username"))
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
    username = html.escape(request.form.get("username"))
    password = request.form.get("password")
    verification = request.form.get("password_confirmation")
    return register(username, password, verification)

@app.route("/register", methods=["GET"])
def register_page():
    return render_index("Registration", "registration_form")

def render_index(banner_title, template_name):
    username = "Guest"
    authenticated = False
    if "auth_token" in request.cookies:
        auth_token = request.cookies.get("auth_token")
        authenticated = "auth_token" in request.cookies
        user = accountCollection.find_one({"auth_token": auth_token})
        if not user is None:
            userContent = dict(user)
            username = userContent.get("username")
        else:
            username = "UserNotFound"
    return render_template(
        "home_page.html",
        authenticated=authenticated, 
        banner_title=banner_title,
        username=username,
        template_name=template_name,
    )

@app.route("/posts", methods=["GET"])
def post_list():
    posts = json.dumps(list_posts()).encode()
    response = make_response()
    response.set_data(posts)
    return response

@app.route("/purge", methods=["GET"])
def purge():
    purge_accounts()
    purge_posts()
    return make_response("", 204)

@app.route("/like/<id>", methods=["POST"])
def like(id):
    auth_token = request.cookies.get("auth_token")
    like_post(id, auth_token)
    return make_response("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)