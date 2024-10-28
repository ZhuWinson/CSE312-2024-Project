from util.accounts import retrieve_account, retrieve_username
from util.database import create_record, delete_record, list_records, retrieve_record, update_record, posts

def create_post(title, message, auth_token):
    title = title
    message = message
    account = retrieve_account(auth_token)
    username = retrieve_username(account)
    post = {"username": username, "title": title, "message": message, "likes": []}
    return create_record(posts, post)

def delete_post(post_id, auth_token):
    account = retrieve_account(auth_token)
    username = retrieve_username(account)
    post = retrieve_post(post_id)
    if post == None or username != post.get("username"):
        return False
    delete_record(posts, post_id)
    return True

def list_posts():
    return list_records(posts)

def purge_posts():
    posts.delete_many({})

def retrieve_post(post_id):
    return retrieve_record(posts, {"id": post_id})

def like_post(id, auth_token):
    account = retrieve_account(auth_token)
    if account is None:
        return
    username = retrieve_username(account)
    post = retrieve_post(id)
    if post is None:
        return
    likes = post.get("likes")
    likes.append(username)
    update_record(posts, post, {"likes": likes})
    print(retrieve_post(id).get("likes"))