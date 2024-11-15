from flask import redirect, make_response, request
from util.database import retrieve_record, accounts
import bcrypt
import hashlib
import secrets

accountCollection = accounts

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
    # If valid password and match then add account to database
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
            #Create authentication auth_token and update account with it
            auth_token = secrets.token_hex(32)
            auth_token_hash = hashlib.sha256(auth_token.encode())
            auth_token_hash = auth_token_hash.hexdigest()
            accountCollection.update_one({"username": username}, {"$set": {"auth_token": auth_token_hash}})
            #Creates redirect and authentication auth_token cookie
            response = make_response(redirect("/"))
            response.set_cookie("auth_token",auth_token,max_age=3600,httponly=True)
            return response
    return redirect("/invalidpassword")

def logout():
    #Find which account is with this auth_token
    auth_token = request.cookies.get("auth_token")
    auth_token = hashlib.sha256(auth_token.encode())
    auth_token = auth_token.hexdigest()
    accountData = accountCollection.find_one({"auth_token": auth_token}, {"_id": 0})
    #Delete auth_token from account and cookie
    if not accountData is None:
        accountData = dict(accountData)
        username = accountData.get("username")
        accountCollection.update_one({"username": username}, {"$set": {"auth_token": None}})
    response = make_response(redirect("/"))
    return response

def purge_accounts():
    accounts.delete_many({})

def retrieve_account(auth_token):
    if auth_token == None:
        return None
    auth_token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
    return retrieve_record(accounts, {"auth_token": auth_token_hash}) 

def retrieve_username(account):
    if account == None:
        return "Guest"
    return account.get("username")