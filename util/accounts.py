from pymongo import MongoClient
from flask import Flask, redirect
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
    specialList = ["!", "@", "#", "$", "%", "^", "&", "(", ")", "-", "_", "="]
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

def register(username, password):
    #Testing purposes
    accountCollection.delete_many({})

    #If valid password then add account to database
    if validate_password(password):
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(password.encode(), salt)
        accountCollection.insert_one({"username": username, "hashedpassword": hashedPassword})
        return redirect("/rTest")
    return redirect("/invalid")

def login(username, password):
    #Find account and check if it exists
    accountData = accountCollection.find_one({"username": username}, {"_id": 0})
    #If account found and password matches
    if not accountData is None:
        accountData = dict(accountData)
        hashedPassword = accountData.get("hashedpassword")
        if bcrypt.checkpw(password.encode(), hashedPassword):
            return redirect("/lTest")
    return redirect("/invalid")