# Python program to find current 
# weather details of any city 
# using openweathermap api 

# import required modules 
import requests, json 
# Enter your API key here 
api_key = "ae56bb2b3e2ff79ba5d5913812925885"
# base_url variable to store url api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
base_url = "http://api.openweathermap.org/data/2.5/weather?"
# Give city name 
city_name = input("Enter city name : ") 
# complete url address 
complete_url = base_url +"q=" + city_name+ "&appid=" + api_key  
# return response object 
response = requests.get(complete_url) 
x = response.json()
if x["cod"] != "404":
	y = x["main"] 
	current_temperature = y["temp"] -273.15
 
	print(" Temperature (in kelvin unit) = " +
              str(current_temperature) )
		 

else: 
	print(" City Not Found ") 
