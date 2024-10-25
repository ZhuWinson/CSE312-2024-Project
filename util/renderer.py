from flask import render_template
from util.accounts import retrieve_account, retrieve_username

def render_home_page(banner_title, template_name, auth_token):
    account = retrieve_account(auth_token)
    authenticated = account != None
    username = retrieve_username(account)
    return render_template(
        "home_page.html",
        authenticated=authenticated, 
        banner_title=banner_title,
        username=username,
        template_name=template_name,
    )