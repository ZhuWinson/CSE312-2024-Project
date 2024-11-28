from util.accounts import retrieve_account, retrieve_username
from util.database import create_record, delete_record, list_records, retrieve_record, update_record, posts
from pathlib import Path
import uuid

recent_age_threshold = 100

def create_post(title, message, file, category, auth_token):
    title = title
    message = message
    account = retrieve_account(auth_token)
    username = retrieve_username(account)
    file_path = None
    mime_type = parse_mime_type(file.filename)
    if file is not None and mime_type is not None:
        file_path = "/static/media/uploads/" + str(uuid.uuid4())
        file.save("." + file_path)
    post = {
        "username": username, 
        "title": title, 
        "message": message,
        "file_path": file_path,
        "mime_type": mime_type,
        "likes": [], 
        "age": 0, 
        "recent": True,
    }
    if category != "":
        post["category"] = category
    post_id = create_record(posts, post)
    post.pop("_id", None)
    post["id"] = post_id
    return post

def delete_post(post_id, auth_token):
    account = retrieve_account(auth_token)
    username = retrieve_username(account)
    post = retrieve_post(post_id)
    if post == None or username != post.get("username"):
        return False
    file_path = post.get("file_path")
    if file_path != None:
        file = Path(file_path)
        file.unlink(True)
    delete_record(posts, {"id": post_id})
    return True

def like_post(post_id, auth_token):
    account = retrieve_account(auth_token)
    if account is None:
        return False
    username = retrieve_username(account)
    post = retrieve_post(post_id)
    if post is None:
        return False
    likes = post.get("likes")
    if username in likes:
        return False
    likes.append(username)
    update_record(posts, {"id": post_id}, {"likes": likes})
    return True

def list_posts(category=None):
    if category is None:
        return list_records(posts, {})
    return list_records(posts, {"category": category})

def list_recent_posts():
    return list_records(posts, {"recent": True})

def parse_mime_type(file_name):
    if "." not in file_name:
        return None
    file_extension = file_name.rsplit('.', 1)[1].lower()
    return mime_types.get(file_extension)

def purge_posts():
    posts.delete_many({})

def purge_uploads():
    directory = Path("./static/media/uploads/")
    for element in directory.iterdir():
        element.unlink()


def retrieve_post(post_id):
    return retrieve_record(posts, {"id": post_id})

def update_post_ages():
    post_list = list_posts()
    for element in post_list:
        post_id = element.get("id")
        age = element.get("age") + 1
        record = {"age": age}
        if age > recent_age_threshold:
            record["recent"] = False
        update_record(posts, {"id": post_id}, record)

mime_types = {
    "gif": "image/gif",
    "jpg": "image/jpeg",
    "mp4": "video/mp4",
    "png": "image/png",
}