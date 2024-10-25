import bcrypt
import hashlib
import uuid
from util.database import create_record, retrieve_record, update_record, accounts

def login_account(username, password):
    account = retrieve_record(accounts, {"username": username})
    if account == None:
        return None
    salt = account.get("salt")
    password_hash = bcrypt.hashpw(password.encode(), salt)
    if password_hash != account.get("password"):
        return None
    auth_token = str(uuid.uuid4())
    auth_token_hash = hashlib.sha256(auth_token.encode()).digest()
    update_record(accounts, account, {"auth_token": auth_token_hash})
    return auth_token

def logout_account(auth_token):
    account = retrieve_account(auth_token)
    if account == None:
        return False
    update_record(accounts, account, {"auth_token": None})
    return True

def purge_accounts():
    accounts.delete_many({})

def register_account(username, password):
    account = retrieve_record(accounts, {"username": username})
    if account != None:
        return None
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
    account = {"username": username, "password": password_hash, "salt": salt}
    return create_record(accounts, account)

def retrieve_account(auth_token):
    if auth_token == None:
        return None
    auth_token_hash = hashlib.sha256(auth_token.encode()).digest()
    return retrieve_record(accounts, {"auth_token": auth_token_hash}) 

def retrieve_username(account):
    if account == None:
        return "Guest"
    return account.get("username")

def validate_password(password):
    if len(password) < 8:
        return False
    special_characters = "!@#$%^&()-_="
    validations = [False, False, False, False]
    for character in password:
        if character.islower():
            validations[0] = True
        elif character.isupper():
            validations[1] = True
        elif character.isnumeric():
            validations[2] = True
        elif character in special_characters:
            validations[3] = True
        else:
            return False
    return all(validations)

"""
from pymongo import MongoClient
from flask import Flask, redirect, make_response, request
import bcrypt
import hashlib
import secrets

mongo_client = MongoClient("mongo")
database = mongo_client["cse312"]
accountCollection = database["account"]

def validate_password(password):
    length = False
    special = False
    lowercase = False
    uppercase = False
    number = False

    #Length == at least 8
    if len(password) >= 8:
        length = True

    #Contains special character
    specialList = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "?"]
    for spec in specialList:
        if password.count(spec) != 0:
            special = True
            break

    #Contains 1 lowercase letter
    #Contains 1 uppercase letter
    #Contains a number
    for character in password:
        if character.islower():
            lowercase = True
        if character.isupper():
            uppercase = True
        if character.isnumeric():
            number = True
        if not character.isalnum():
            if not character in specialList:
                return False

    return length and special and lowercase and uppercase and number

def register(username, password, verification):
    # If valid password and match then add account to database
    if not validate_password(password):
        return redirect("/invalidpassword")
    if not password ==  verification:
        return redirect("/passwordmismatch")

    #Check if username == taken
    existingUser = accountCollection.find_one({"username": username})
    if existingUser == None:
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(password.encode(), salt)
        accountCollection.insert_one({"username": username, "hashedpassword": hashedPassword})
        return redirect("/")
    else:
        return redirect("/usertaken")

def login(username, password):
    #Find account and check if it exists
    accountData = accountCollection.find_one({"username": username}, {"_id": 0})
    #If account found and password matches
    if not accountData == None:
        accountData = dict(accountData)
        hashedPassword = accountData.get("hashedpassword")
        if bcrypt.checkpw(password.encode(), hashedPassword):
            #Create authentication token and update account with it
            auth_token = secrets.token_hex(32)
            auth_token = hashlib.sha256(auth_token.encode())
            auth_token = auth_token.hexdigest()
            accountCollection.update_one({"username": username}, {"$set": {"token": auth_token}})
            #Creates redirect and authentication token cookie
            response = make_response(redirect("/"))
            response.set_cookie("token",auth_token,max_age=3600,httponly=True)
            return response
    return redirect("/invalid")

def logout():
    #Find which account == with th== token
    auth_token = request.cookies.get("token")
    auth_token = hashlib.sha256(auth_token.encode())
    auth_token = auth_token.hexdigest()
    accountData = accountCollection.find_one({"token": auth_token}, {"_id": 0})
    #Delete token from account and cookie
    if not accountData == None:
        accountData = dict(accountData)
        username = accountData.get("username")
        accountCollection.update_one({"username": username}, {"$set": {"token": ""}})
    response = make_response(redirect("/"))
    response.set_cookie("token", "", max_age=0)
    return response

def display_username():
    pass
"""