import requests
import json
import os
from datetime import datetime

def multi_API():

    now  = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    filename = "Week 2/Day 3/Multi_API_Files/record.json"
    fn = "Week 2/Day 3/Multi_API_Files/dashboard_snapshots.json"
    API_report = "Week 2/Day 3/Multi_API_Files/Multi_API_Report.txt"

    
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

    def fetch_all_data(city):
        u_curr = "https://api.exchangerate-api.com/v4/latest/USD"
        u_user = "https://randomuser.me/api/?results=5"
        u_weat = f"https://wttr.in/{city}?format=j1"
    
        urls = [u_curr, u_user, u_weat]
        data = {}

        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                data[url] = response.json()

        w_raw = data.get(u_weat)
        weather = {
        'Date': w_raw['weather'][0]['date'],
        'temperature in C': w_raw['current_condition'][0]['temp_C'],
        'temperature in F': w_raw['current_condition'][0]['temp_F'] 
        } if w_raw else None

        c_raw = data.get(u_curr)
        currency = {'USD': c_raw['rates']['USD']} if c_raw else None

        u_raw = data.get(u_user)
        users_list = []
        if u_raw and u_raw.get('results'):
            for row in u_raw['results']:
                users_list.append({
                "Name": f"{row['name']['title']} {row['name']['first']} {row['name']['last']}",
                "Email": row['email'],
                "Age": row['dob']['age'],
                "Gender": row['gender'],
                "Location": f"{row['location']['street']['number']} {row['location']['street']['name']}",
                "Nationality": row['location']['country']
                })

        all_data = {
        'Generated on': timestamp,
        'weather': weather,
        'currency': currency,
        'users': users_list if users_list else None
        }

        print(all_data)
        return all_data

    def create_dashboard(city):

        c = "https://api.exchangerate-api.com/v4/latest/USD"
        r = "https://randomuser.me/api/?results=5"
        w = f"https://wttr.in/{city}?format=j1"

        try:
            all_currency = None
            user_info = None
            content = None
            users = []
            dash = []

            if not os.path.exists(fn):
                with open(fn,"w") as file:
                    json.dump([], file)

            response1 = requests.get(c)
            response2 = requests.get(r)
            response3 = requests.get(w)

            r1 = response1.json() if response1.status_code == 200 else None
            r2 = response2.json() if response2.status_code == 200 else None
            r3 = response3.json() if response3.status_code == 200 else None

            curr = r1['rates']
            rand = r2['results']
            weat = r3['current_condition'][0]
            weat_cond = r3['weather'][0]

            if os.path.exists(fn) and os.path.getsize(fn):
                with open(fn, "r") as file:
                    dash = json.load(file)

            if len(curr)>0:
                all_currency = curr

            if len(rand)>0:
                for row in rand:
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

                    users.append(user_info)

            if len(weat)>0 and len(weat_cond)>0:
                date = weat_cond['date']
                tempC = weat['temp_C']
                tempF = weat['temp_F']
                avgC = weat_cond['avgtempC']
                avgF = weat_cond['avgtempF']
                maxC = weat_cond['maxtempC']
                maxF = weat_cond['maxtempF']
                minC = weat_cond['mintempC']
                minF = weat_cond['mintempF']

                content = {
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

            dashboard = {
                'Generated on': timestamp,
                'User information': users if users else user_info,
                'Weather information': content,
                'Currency based on regions': all_currency
            }
            
            dash.append(dashboard)
            

            if os.path.exists(fn):
                with open(fn, "w") as file:
                    json.dump(dash,file,indent = 4)

        except Exception as e:
            print(f"Dashboard error: {e}")

    def list_snapshots(city):
        try:    
            if os.path.exists(fn) and os.path.getsize(fn):
                with open(fn, "r") as file:
                    reader = json.load(file)
                    for row in reader:
                        weat = row['Weather information']
                        curr = row['Currency based on regions']
                        all = curr
                        if city in weat['City']:
                            print("Snapshot found...")
                            print(f"Fetching details for city {city}")
                            print(f"Date: {weat['Date']}")
                            print(f"Temperature in C: {weat['temperature in C']['temperature']},\n average: {weat['temperature in C']['average temperature']}, maximum: {weat['temperature in C']['maximum temperature']}, minimum: {weat['temperature in C']['minumum temperature']}")
                            print(f"Temperature in F: {weat['temperature in F']['temperature']},\n average: {weat['temperature in F']['average temperature']}, maximum: {weat['temperature in F']['maximum temperature']}, minimum: {weat['temperature in F']['minumum temperature']}")
                            print(f"User info: {row['User information']}")
                            print(f"Currency based on regions:")
                            for k,v in all.items():
                                print(f"{k}: {v}")

        except Exception as e:
            print(f"List snapshot error: {e}")

    def compare_snapshots(city1, city2):
        try:
            snap1 = None
            snap2 = None
            if os.path.exists(fn):
                with open(fn, "r") as file:
                    reader = json.load(file)
                    for row in reader:
                        weat = row.get('Weather information', {})
                        if city1.title() == weat.get('City'):
                            snap1 = weat

                        if city2.title() == weat.get("City"):
                            snap2 = weat
                            Date2 = snap2['Date']

                    if snap1 is None or snap2 is None:
                        missing = city1 if not snap1 else city2
                        print(f"Error: {missing} was not found in the database.")
                        return
                        
                    Date = snap1['Date']
                    tempC = int(snap1['temperature in C']['temperature'])
                    tempF = int(snap1['temperature in F']['temperature'])
                    maxC = int(snap1['temperature in C']['maximum temperature'])
                    maxF = int(snap1['temperature in F']['maximum temperature'])
                    minC = int(snap1['temperature in C']['minumum temperature'])
                    minF = int(snap1['temperature in F']['minumum temperature'])
                    avgC = int(snap1['temperature in C']['average temperature'])
                    avgF = int(snap1['temperature in F']['average temperature'])


                    tempC2 = int(snap2['temperature in C']['temperature'])
                    tempF2 = int(snap2['temperature in F']['temperature'])
                    maxC2 = int(snap2['temperature in C']['maximum temperature'])
                    maxF2 = int(snap2['temperature in F']['maximum temperature'])
                    minC2 = int(snap2['temperature in C']['minumum temperature'])
                    minF2 = int(snap2['temperature in F']['minumum temperature'])
                    avgC2 = int(snap2['temperature in C']['average temperature'])
                    avgF2 = int(snap2['temperature in F']['average temperature'])

                citydiff = "Same Cites" if city1 == city2 else "Different City Name"
                datediff = "Same dates" if Date == Date2 else "Different dates"
                tempCd = tempC - tempC2
                tempFd = tempF - tempF2
                tempmaxC = maxC - maxC2
                tempminC = minC - minC2
                tempmaxF = maxF - maxF2
                tempminF = minF - minF2
                tempavgC = avgC - avgC2
                tempavgF = avgF - avgF2


                report = f"""
*****************************************************************************************************************
                                        SNAPSHOT COMPARISON                 Data generated on: {timestamp}                                     
*****************************************************************************************************************
|      FIELD           |      SNAPSHOT 1        |      SNAPSHOT 2        |       Difference       |
|______________________|________________________|________________________|________________________|
| CITY                 | {city1:<22} | {city2:<22} | {citydiff:<22} |
|______________________|________________________|________________________|________________________|
| DATE                 | {Date:<22} | {Date2:<22} | {datediff:<22} |
|______________________|________________________|________________________|________________________|
| Temp (C)             | {tempC:<22} | {tempC2:<22} | {tempCd:<22} |
|______________________|________________________|________________________|________________________|
| Temp (F)             | {tempF:<22} | {tempF2:<22} | {tempFd:<22} |
|______________________|________________________|________________________|________________________|
| Max Temp (C)         | {maxC:<22} | {maxC2:<22} | {tempmaxC:<22} |
|______________________|________________________|________________________|________________________|
| Min Temp (C)         | {minC:<22} | {minC2:<22} | {tempminC:<22} |
|______________________|________________________|________________________|________________________|
| Max Temp (F)         | {maxF:<22} | {maxF2:<22} | {tempmaxF:<22} |
|______________________|________________________|________________________|________________________|
| Min Temp (F)         | {minF:<22} | {minF2:<22} | {tempminF:<22} |
|______________________|________________________|________________________|________________________|
| Avg Temp (C)         | {avgC:<22} | {avgC2:<22} | {tempavgC:<22} |
|______________________|________________________|________________________|________________________|
| Avg Temp (F)         | {avgF:<22} | {avgF2:<22} | {tempavgF:<22} |
|______________________|________________________|________________________|________________________|
"""   
            if not os.path.exists(API_report):
                with open(API_report, "w") as file:
                    file.write("Hello")

            if os.path.exists(API_report):
                with open(API_report, "w") as file:
                    file.write(report)

            print(f"Please view the report saved on path : {API_report}")
            
        except Exception as e:
            print(f"Comparison failed: {e}")

    while True:

        print("*"*20)
        print("MULTI API DASHBOARD")
        print("*"*20)
        print("1. Generate Weather Data")
        print("2. Generate Currency Data")
        print("3. Generate Random users")
        print("4. Display Data based on City")
        print("5. Create Dashboard")
        print("6. Filter Snapshots based on city")
        print("7. Compare Snapshots")
        print("8. View Reports")
        print("9. Quit")

        choice = input("Enter a valid choice from 1 to 9: ")

        if choice == "1":
            name = input("Enter the city name: ")
            city = name.title()

            weather_json = generate_weather(city)

            if weather_json:
                fetch_weather_data(weather_json,city)

        elif choice == "2":
            fetch_currency_data()

        elif choice == "3":
            count = int(input("Enter the count of users you want to generate: "))
            fetch_user_data(count)

        elif choice == "4":
            name = input("Enter the city name: ")
            city = name.title()
            fetch_all_data(city)

        elif choice == "5":
            name = input("Enter the city name: ")
            city = name.title()
            create_dashboard(city)

        elif choice == "6":
            name = input("Enter the city name: ")
            city = name.title()
            list_snapshots(city)

        elif choice == "7":
            c1 = input("Enter the name of the first city: ")
            city1 = c1.title()
            c2 = input("Enter the name of second city: ")
            city2 = c2.title()
            compare_snapshots(city1, city2)

        elif choice == "8":
            if os.path.exists(API_report):
                with open(API_report, "r") as file:
                    reader = file.read()
                    print(reader)

        elif choice == "9":
            print("Quitting....")
            break

        else:
            print("Invalid entry")

        

multi_API()
