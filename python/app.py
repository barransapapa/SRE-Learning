# from flask import Flask, request

# app= Flask(__name__)

# @app.route('/') #These are the paths on the link
# def hello_world():
#     return 'Hello, World!'

# stores = [

#     {
#         'name': 'My Store',
#         'items': [
#             {
#                 'name': 'Chair',
#                 'price': 15.99
#             }
#         ]
#     }
# ]

# @app.get('/store') #http://127.0.0.1:5000/store
# def get_stores():
#     return {'stores': stores}

# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=8000)

# Reference: https://apidog.com/es/blog/how-to-use-nasa-api-3/#servicio-web-de-objetos-cercanos-a-la-tierra-neows
import requests

api_key = "<API_Key>"
#Defines the request
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2025-09-12&end_date=2025-09-12&api_key={api_key}"

#Get data
response = requests.get(url)
data = response.json()
print("Keys are: " + str(data.keys()))


for date, asteroids in data ["near_earth_objects"].items():
    print(f"Asteroids on {date}:")
    for asteroid in asteroids: 
        print(f"- {asteroid['name']}: It was close to the earth: {asteroid['is_potentially_hazardous_asteroid']}, Velocity: {asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']} km/h")