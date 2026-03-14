import os
import json
from datetime import datetime,timedelta
import requests

def weather():

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    filename = "Python-practice/week 2/Day 3/Weather_files/weather.json"

    def generate_weather(city):
        try:
            url = f"https://wttr.in/{city}?format=j1"

            if not os.path.exists(filename):
                with open(filename, "w") as file:
                    json.dump([],file)
                print(f"File created at {filename} on {timestamp}")

            response = requests.get(url)
            if response.status_code == 200:
                return response.json()

        except Exception as e:
            print(f"Error: {e}")

    def get_weather(data,city):
        try:
            current = data['current_condition'][0]
            region = data['nearest_area'][0]['country'][0]['value']
            temp_c = current.get("temp_C")
            temp_f = current.get("temp_F")

            print(f"City: {city}")
            print(f"Country: {region}")
            print(f"Temperature in Celsius: {temp_c}")
            print(f"Temperature in farenheit: {temp_f}")
                
        except Exception as e:
            print(f"Error: {e}")

    def display_current_weather(data,city):
        try:
            exclude = ['weatherDesc','weatherIconUrl']
            curr = data['current_condition'][0]
            print(f"Current weather conditions for {city}:")
            for k,v in curr.items():
                if k not in exclude:
                    print(f"{k.replace('_',' ').title()}: {v}")

        except Exception as e:
            print(f"Weather unavailable: {e}")

    def display_forecast(data, city):
        try:
            forecast = []
            time = data.get('weather',[])
            try:
                with open(filename, "r") as file:
                    forecast = json.load(file)
                if not isinstance(forecast, list):
                    forecast = [forecast]
            except (FileNotFoundError, json.JSONDecodeError):
                forecast = []
            count = int(input(f"Enter the count of days you want to view the forecast(available days: {len(time)}): "))
            for x in range(min(count,len(time))):
                day_date = time[x]
                date = day_date.get('date')
                max_t = day_date.get('maxtempC')
                min_t = day_date.get('mintempC')
                max_f = day_date.get('maxtempF')
                min_f = day_date.get('mintempF')
                print(f"Date: {date}")
                print(f"Maximum temperature in celsius: {max_t}")
                print(f"Minimum temperature in celsius: {min_t}")
                print(f"Maximum temperature in farenheit: {max_f}")
                print(f"Minimum temperature in farenheit: {min_f}\n")

                content = {
                    "Generated on": timestamp,
                    "City" : city,
                    "Date": date,
                    "Maximum temperature in celsius": max_t,
                    "Minimum temperature in celsius": min_t,
                    "Maximum temperature in farenheit": max_f,
                    "Minimum temperature in farenheit": min_f
                }

                forecast.append(content)

            with open(filename, "w") as file:
                json.dump(forecast,file,indent=4)

            print(f"Data saved to path: {filename}")

        except Exception as e:
            print(f"Forecast Unavailable: {e}")

    def view_history():
        try:
            if os.path.exists(filename) and os.path.getsize(filename)>0:
                with open(filename, "r") as file:
                    reader = json.load(file)
                    print(f"File found on path: {filename}")
                    print("Fetching saved details from inventory.....")
                    print("----TEMPERATURE HISTORY----")
                    for row in reader:
                            print(f"Generated on: {row['Generated on']}")
                            print(f"City: {row['City']}")
                            print(f"Date: {row['Date']}")
                            print(f"Maximum temperature in celsius: {row['Maximum temperature in celsius']}")
                            print(f"Minimum temperature in celsius: {row['Minimum temperature in celsius']}")
                            print(f"Maximum temperature in farenheit: {row['Maximum temperature in farenheit']}")
                            print(f"Minimum temperature in farenheit: {row['Minimum temperature in farenheit']}\n")
        
        except Exception as e:
            print(f"History unavailable: {e}")

    def compare_history():
        try:
            count = int(input("Enter the number of cities you want to compare the temperature of: "))
            
            for i in range(count):
                c = input(f"Enter City {i+1}: ")
                city = c.title()
                url = f"https://wttr.in/{city}?format=j1"
                response = requests.get(url)
                if response.status_code==200:
                    data = response.json()
                    date = data['weather'][0]['date']
                    min_tempC = data['weather'][0]['mintempC']
                    max_tempC = data['weather'][0]['maxtempC']
                    min_tempF = data['weather'][0]['mintempF']
                    max_tempF = data['weather'][0]['maxtempF']
                    print(f"City: {city}")
                    print(f"Date: {date}")
                    print(f"Maximum temperature in Celsius: {max_tempC}")
                    print(f"Minimum temperature in Celsius: {min_tempC}")
                    print(f"Maximum temperature in Farenheit: {max_tempF}")
                    print(f"Minimum Temperature in Farenheit: {min_tempF}\n")

        except Exception as e:
            print(f"Error: {e}")

    while True:
        print("-------WEATHER FORECAST DATABASE-------")
        print("1. Check current weather")
        print("2. View 3 day forecast")
        print("3. Compare cities")
        print("4. View search history")
        print("5. Quit")

        choice = input("Enter the choice from 1 to 5: ")

        if choice == "1":
            name = input("Enter the city you want to know the temperature of: ")
            city = name.title()
            weather_json = generate_weather(city)
            if weather_json:
                display_current_weather(weather_json,city)

        if choice == "2":
            name = input("Enter the city you want to know the temperature of: ")
            city = name.title()
            weather_json = generate_weather(city)
            if weather_json:
                display_forecast(weather_json, city)

        if choice == "3":
            compare_history()

        if choice == "4":
            view_history()

        if choice == "5":
            print("Quitting....")
            break
        
weather()