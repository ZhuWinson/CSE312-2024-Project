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

    #Length is at least 8
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
    # #`Testing purposes
    # accountCollection.delete_many({})

    # If valid password then add account to database
    if not validate_password(password):
        return redirect("/invalidpassword")
    if not password == verification:
        return redirect("/passwordmismatch")
    #Check if username is taken
    existingUser = accountCollection.find_one({"username": username})
    if existingUser is None:
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
    if not accountData is None:
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
    #Find which account is with this token
    auth_token = request.cookies.get("token")
    auth_token = hashlib.sha256(auth_token.encode())
    auth_token = auth_token.hexdigest()
    accountData = accountCollection.find_one({"token": auth_token}, {"_id": 0})
    #Delete token from account and cookie
    if not accountData is None:
        accountData = dict(accountData)
        username = accountData.get("username")
        accountCollection.update_one({"username": username}, {"$set": {"token": ""}})
    response = make_response(redirect("/"))
    response.set_cookie("token", "", max_age=0)
    return response

