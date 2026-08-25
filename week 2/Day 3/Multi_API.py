import requests
import json
import os
from datetime import datetime

def multi_API():

    now  = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    filename = "Python-practice/week 2/Day 3/dashboard_snapshots.json"

    
    currency = "https://api.exchangerate-api.com/v4/latest/USD"
    random = "https://randomuser.me/api/?results=5"

    def generate_weather(city):
        try:
            weather = f"https://wttr.in/{city}?format=j1"
            if not os.path.exists(filename):
                with open(filename, "w") as file:
                    json.dump([],file)

            response = requests.get(weather)
            if response.status_code == 200:
                return response.json()

        except Exception as e:
            print(f"Fetch error: {e}")

    def fetch_weather_data(data, city):
        try:
            temp=[]
            all = {}
            if os.path.exists(filename) and os.path.getsize(filename)>0:
                with open(filename, "r") as file:
                    temp = json.load(file)

            current = data['current_condition'][0]
            weather_cond = data['weather'][0]

            print(f"Fetching weather data for {city}...")
            print(f"City Name: {city}")

            date = weather_cond['date']
            tempC = current['temp_C']
            tempF = current['temp_F']
            avgC = weather_cond['avgtempC']
            avgF = weather_cond['avgtempF']
            maxC = weather_cond['maxtempC']
            maxF = weather_cond['maxtempF']
            minC = weather_cond['mintempC']
            minF = weather_cond['mintempF']

            print(f"Date: {date}")
            print(f"Data in Celsius temperature- live: {tempC}, maximum: {maxC}, minimum: {minC}, average: {avgC} ")
            print(f"Data in Farenheit temperature- live: {tempF}, maximum: {maxF}, minimum: {minF}, average: {avgF}")
            print(f"Data generated on: {timestamp}")

            content = {
                "Generated on": timestamp,
                "City": city,
                "Date" : date,
                "temperature in C" : {
                    "temperature": tempC,
                    "average temperature": avgC,
                    "maximum temperature": maxC,
                    "minumum temperature": minC
                },
                "temperature in F" : {
                    "temperature": tempF,
                    "average temperature": avgF,
                    "maximum temperature": maxF,
                    "minumum temperature": minF
                }    
            }

            temp.append(content)

            with open(filename, "w") as file:
                json.dump(temp,file,indent = 4)

        except Exception as e:
            print(f"Weather fetch error: {e}")

    def fetch_currency_data():
        try:
            cny = []
            mark = "None"
            all = None
            with open(filename, "r") as file:
                cny = json.load(file)
            response = requests.get(currency)
            if response.status_code == 200:
                data = response.json()
                rates = data['rates']
                found = False

            while True:
                curr = input("Do you want rate of a specific region or all rates? type 'S' for specific region, 'A' for all regions and 'Q' to quit: ")
                if curr == 'S' or curr == 's':
                        m = input("Enter the region you want to view the rate of with 3 letter acronym: ")
                        mark = m.upper()
                        for row in rates:
                            if mark in rates and len(mark) == 3:
                                print(f"Rate for region {mark} is {rates[mark]}")
                                break
                            else:
                                print(f"value entered does not match with the existing data.")
                                break
                elif curr == 'A' or curr == 'a':
                    all = rates
                    for k,v in rates.items():
                        print(f"{k}: {v}")

                else:
                    break
                
            content = {
                "Data generated on": timestamp,
                "Specific region": {
                    "Region Name": mark,
                    "Rate": rates[mark]
                },
                "All regions": all if all else "Not Requested by user"
                
            }

            cny.append(content)

            with open(filename, "w") as file:
                json.dump(cny, file, indent = 4)

        except Exception as e:
            print(f"Weather fetch error: {e}")

    def fetch_user_data(count):
        try:
            total_users = []

            with open(filename, "r") as file:
                total_users= json.load(file)

            parameter = {
                "result" : count
            }

            response = requests.get(random, params=parameter)
            if response.status_code == 200:
                data = response.json()
                users = data['results']

                for row in users:
                    name = f"{row['name']['title']} {row['name']['first']} {row['name']['last']}"
                    email = row['email']
                    age = row['dob']['age']
                    gender = row['gender']
                    nationality = row['location']['country']
                    location = f"{row['location']['street']['number']} {row['location']['street']['name']}"

                    user_info = {
                    "Generated on": timestamp,
                    "User info":{
                        "name": name,
                        "email" : email,
                        "age": age,
                        "gender": gender,
                        "nationality": nationality,
                        "location": location
                        }    
                    }

                    total_users.append(user_info)

            with open(filename, "w") as file:
                json.dump(total_users, file, indent = 4)


        except Exception as e:
            print(f"User details not found: {e}")

    # def fetch_user_data(count = 5):
    #     try:


    #     except Exception as e:
    #         print(f"Data not found; {e}")

    # name = input("Enter the city name: ")
    # city = name.title()

    # weather_json = generate_weather(city)

    # if weather_json:
    #     fetch_weather_data(weather_json,city)

    #fetch_currency_data()

    fetch_user_data(count = 5)
        

multi_API()