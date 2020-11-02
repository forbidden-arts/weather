import urllib.request, json, requests
from datetime import datetime

# Get location based on IP address, store latitude and longitude.
def get_location():
	with urllib.request.urlopen("https://geolocation-db.com/json") as url:
	    data = json.loads(url.read().decode())
	location = []
	location.append(data['latitude'])
	location.append(data['longitude'])
	return location

# Hit the OWM Onecall API, response comes in JSON. Is stored as a multi-layered dictionary.
def get_weather(loc):
	weather = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + str(home[0]) + "&lon=" + str(home[1]) + "&units=metric&appid=" + apikey)
	return weather.json()

# Convert from UNIX time to something understandable.
def readable_time(dt):
	readable = datetime.utcfromtimestamp(dt).strftime('%H:%M:%S %d-%m-%Y')
	return readable

# Define weather terms/
def weather_terms(cloud):
	if cloud >= 80:
		return "cloudy"
	elif cloud >= 60:
		return "mostly cloudy"
	elif cloud >= 40:
		return "partly cloudy"
	elif cloud >= 20:
		return "mostly sunny"
	else:
		return "sunny"

# Hourly forcast for next N hours
def hourly_forecast2(n):
	for hours in weather['hourly'][:n + 1]:
		print("At", readable_time(hours['dt']+weather['timezone_offset'])[:8], "it will be", str(round(hours['temp'], 1)), "and", weather_terms(hours['clouds']), end="")
		if hours['pop'] >= .5 and ('rain' in hours.keys() or 'snow' in hours.keys()):
			print(" and likely to", hours['weather'][0]['main'].lower() + ".") # " and likely to", 
		elif hours['pop'] >= .25 and ('rain' in hours.keys() or 'snow' in hours.keys()):
			print(" with a chance of", hours['weather'][0]['main'].lower() + ".") # " with a chance of", 
		else:
			print(".")

def hourly_forecast(n):
	for hours in weather['hourly'][:n + 1]:
		print(hours)

# Find sun
def next_sun(sb):
	for hours in weather['hourly']:
		if hours['clouds'] < 40: # check whether there's less than 40% clouds forecasted. only count hours during the day.
			if hours['dt'] in range(weather['current']['sunrise'], weather['current']['sunset']) or hours['dt'] in range(weather['daily'][1]['sunrise'], weather['daily'][1]['sunset']):
				sb.append(1)
			else:
				sb.append(-1)
		else:
			sb.append(0)
	if 1 not in sb:
		print("Days will be cloudy for the next 48 hours.")
	else:
		stime = 0
		for st in sb:
			if st == 1:
				stime += 1
			elif st == 0 and stime != 0:
				break
			else:
				pass
		print("Sunny skies predicted at", str(readable_time(weather['hourly'][sb.index(1)]['dt'] + weather['timezone_offset'])), "which will last for", str(stime), "hours.")
		print(sb)



# API Key:  4134492269497d50deb41b893bab3cb9
home = []
sunshine = []
apikey = "4134492269497d50deb41b893bab3cb9"

# Figure out where we are, and get our weather info.
try:
	home = get_location()
except:
	print("Could not determine location.")
	exit()

try:
	weather = get_weather(home)
except:
	print("Could not fetch weather.")
	exit()


print("\nThe current time is:", readable_time(weather['current']['dt'] + weather['timezone_offset']))
print("It is currently", str(weather['current']['temp']), "degrees celcius and", weather_terms(weather['current']['clouds']) + ".")
# print(weather['current']['clouds'])

#hourly_forecast(48)

next_sun(sunshine)
#print(weather['hourly'])

#hourly_forecast(4)
#print(weather)