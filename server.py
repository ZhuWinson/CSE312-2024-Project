from flask import Flask, make_response, redirect, request
from flask_socketio import SocketIO, emit
from util.accounts import register, login, logout, purge_accounts
from util.posts import create_post, delete_post, like_post, list_posts, list_recent_posts
from util.posts import purge_posts, purge_uploads, retrieve_post, update_post_ages
from util.renderer import render_home_page
import atexit
import html
import json
import os
import threading
import time

app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app)

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

@app.route("/home/<category>", methods=["GET"])
def category_page(category):
    auth_token = request.cookies.get("auth_token")
    return render_home_page("/" + category, "post_list", auth_token)

@app.route("/create", methods=["POST"])
def create():
    auth_token = request.cookies.get("auth_token")
    title = html.escape(request.form.get("title", ""))
    message = html.escape(request.form.get("message", ""))
    file = request.files.get("upload")
    category = html.escape(request.form.get("category", ""))
    category = category.replace(" ", "")
    category = category.lower()
    #Send to all connected clients via websockets
    post = create_post(title, message, file, category, auth_token)
    socketio.emit("post", post)
    return redirect("/home/" + category)

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
@app.route("/home", methods=["GET"])
@app.route("/home/", methods=["GET"])
def home_page():
    return redirect("/home/recent")

@app.route("/like/<id>", methods=["POST"])
def like(id):
    auth_token = request.cookies.get("auth_token")
    like_post(id, auth_token)
    return make_response("", 204)

@app.route("/login", methods=["POST"])
def login_submit():
    username = html.escape(request.form.get("username"))
    password = request.form.get("password")
    return login(username, password)

@app.route("/login", methods=["GET"])
def login_page():
    auth_token = request.cookies.get("auth_token")
    return render_home_page("Login", "login_form", auth_token)

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
    auth_token = request.cookies.get("auth_token")
    return render_home_page("Register", "registration_form", auth_token)

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
    dev_mode = os.environ.get("DEV_MODE")
    if dev_mode != "enabled":
        return make_response("", 404)
    purge_accounts()
    purge_posts()
    purge_uploads()
    return redirect("/")

def update():
    while True:
        update_post_ages()
        time.sleep(1)

@socketio.on("connect")
def ws_handshake():
    print("Client Connected")

@socketio.on('delete')
def ws_delete_post(post_id):
    auth_token = request.cookies.get("auth_token")
    authorized = delete_post(post_id, auth_token)
    if authorized:
        emit('remove', post_id, broadcast=True)

@socketio.on('like')
def ws_like_post(post_id):
    auth_token = request.cookies.get("auth_token")
    authorized = like_post(post_id, auth_token)
    if authorized:
        post = retrieve_post(post_id)
        emit('update', post, broadcast=True)

if __name__ == "__main__":
    thread = threading.Thread(target=update)
    thread.start()
    atexit.register(lambda: thread.join())
    # Websockets Start (UNSAFE FOR NOW)
    # use_reloder is now False!!!!!!
    # this is necessary for threading work properly
    # if you are experiencing bugs, try setting use_reloader to True
    socketio.run(app,host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True, use_reloader=False)