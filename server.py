from flask import Flask, make_response, redirect, render_template, request
from util.accounts import register, login, logout, purge_accounts, accountCollection
from util.posts import create_post, delete_post, like_post, list_posts, list_recent_posts
from util.posts import purge_posts, update_post_ages
from util.renderer import render_home_page
import atexit
import html
import json
import threading
import time

app = Flask(__name__, static_url_path="/static")

@app.after_request
def after_request(response):
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
    category = html.escape(request.form.get("category", ""))
    category = category.replace(" ", "")
    category = category.lower()
    create_post(title, message, category, auth_token)
    return redirect("/" + category)

@app.route("/create", methods=["GET"])
def create_page():
    auth_token = request.cookies.get("auth_token")
    return render_home_page("Create Post", "create_form", auth_token)

@app.route("/posts/<id>", methods=["DELETE"])
def delete(id):
    auth_token = request.cookies.get("auth_token")
    authorized = delete_post(id, auth_token)
    if authorized == False:
        response = make_response("", 403)
        return response
    return make_response("", 204)

@app.route("/", methods=["GET"])
def home_page():
    return redirect("/recent")

@app.route("/<category>", methods=["GET"])
def home_page_category(category):
    if category == "":
        category = "recent"
    auth_token = request.cookies.get("auth_token")
    return render_home_page("/" + category, "post_list", auth_token)

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

@app.route("/posts/<category>", methods=["GET"])
def post_list(category):
    category = html.escape(category)
    post_list = None
    if category == "recent":
        post_list = list_recent_posts()
    else:
        post_list = list_posts(category)
    post_list = json.dumps(post_list).encode()
    response = make_response()
    response.set_data(post_list)
    return response

@app.route("/purge", methods=["GET"])
def purge():
    purge_accounts()
    purge_posts()
    return redirect("/")

@app.route("/like/<id>", methods=["POST"])
def like(id):
    auth_token = request.cookies.get("auth_token")
    like_post(id, auth_token)
    return make_response("", 204)

def update():
    update_post_ages()
    time.sleep(1)
    update()

# use_reloder is now False!!!!!!
# this is necessary for threading work properly
# if you are experiencing bugs, try setting use_reloader to True
if __name__ == "__main__":
    thread = threading.Thread(target=update)
    thread.start()
    atexit.register(lambda: thread.join())
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)