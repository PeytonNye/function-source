"""
__author__ = "Meshcomm Engineering"
__copyright__ = "Copyright (C) 2023 Meshcomm Engineering"
__version__ = '2.0'
__version__ = "20230220"

post_request.py
7/20/2023
Gets the wifi name and password from the user and sends them to the specified unit

"""
#Libraries
import requests

#Libraries for security code
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import auth
# from google.cloud import firestore
# import firebase_functions
# import json
# import functions_framework
# import flask

# Initialize the Firebase app with your credentials
# cred = credentials.Certificate('firebase_key.json')
# firebase_admin.initialize_app(cred)


config = {
  "apiKey": "AIzaSyBrifILObHZWloc3hRXN44Oww5msqPE_rg",
  "authDomain": "awesome-db-ccc92.firebaseapp.com",
  "databaseURL": "https://awesome-db-ccc92.firebaseio.com",
  "storageBucket": "awesome-db-ccc92.appspot.com",
  "serviceAccount": "key.json"
}


"""
Security code

Obtains user's ID token to authenticate user

"""
# # Authenticate the user and obtain the ID token
# user = auth.create_user()

# # id_token = user.get_id_token()


# custom_token = auth.create_custom_token('7OA0ukaM1wbjl52dwzbPgUE0TZG3')
# request_data = {
#             "token": custom_token.decode("utf-8"),
#             "returnSecureToken": True
#         }

# response = requests.post(url, json=request_data)
# id_token = response.json().get("idToken")

# # id_token = auth.get_auth().verify_id_token(custom_token)


# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': b"Bearer" + id_token
#     }


URL = "https://wifi-config-r22avn37ea-uc.a.run.app"

data = {'cpuid': '322239d75d48b311',
        'ssid': 'verygoodwifi',
        'password': 'sfdase1223492rwehejfaser'}

#creates post request with the user's cpuid, ssid, and password
response = requests.post(URL, data=data, timeout=10, params=data)

#prints response number (200 = success)
print(response)

# print content of request
print(response.content)
