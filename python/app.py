import requests
from flask import Flask, request

app = Flask(__name__)
@app.route('/') #These are the paths on the link
def hello_world():
    return 'Hello, World!'

@app.get('/asteroids') #http://127.0.0.1:5000/asteroids
def get_asteroids():
    #api_key = "<API_Key>"
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2025-09-12&end_date=2025-09-12&api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    return {"data": data}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)

# Reference: https://apidog.com/es/blog/how-to-use-nasa-api-3/#servicio-web-de-objetos-cercanos-a-la-tierra-neows
# for date, asteroids in data ["near_earth_objects"].items():
#     print(f"Asteroids on {date}:")
#     for asteroid in asteroids: 
#         print(f"- {asteroid['name']}: It was close to the earth: {asteroid['is_potentially_hazardous_asteroid']}, Velocity: {asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']} km/h")