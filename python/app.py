import requests
from datetime import date
from flask import Flask
from getpass import getpass

# This is a simple Flask web application that provides an endpoint to retrieve data about asteroids from NASA's NeoWs API.
# Initialize Flask app
app = Flask(__name__)
# The line below prompts the user to enter their NASA API key securely. You can get your own API key by registering at https://api.nasa.gov/.
api_key = getpass("Enter your NASA API Key: ")
@app.route('/') #These are the paths on the link
def hello_world():
    return 'Please go to the /asteroids endpoint to see data about asteroids from NASA NeoWs API.'+ 'test'


#This endpoint retrieves data about asteroids from NASA's NeoWs API
@app.get('/asteroids') #http://127.0.0.1:8000/asteroids
def get_asteroids():
    #Get today's date in YYYY-MM-DD format
    search_date=date.today().strftime("%Y-%m-%d")
    #Make a GET request to the NASA NeoWs API to retrieve asteroid data for the specified date
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={search_date}&end_date={search_date}&api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    return {"data": data}
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

# Reference: https://apidog.com/es/blog/how-to-use-nasa-api-3/#servicio-web-de-objetos-cercanos-a-la-tierra-neows
# for date, asteroids in data ["near_earth_objects"].items():
#     print(f"Asteroids on {date}:")
#     for asteroid in asteroids: 
#         print(f"- {asteroid['name']}: It was close to the earth: {asteroid['is_potentially_hazardous_asteroid']}, Velocity: {asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']} km/h")
