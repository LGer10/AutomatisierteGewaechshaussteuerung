# automatisiertes gewächshaus | main script | version 0.1

# import libraries
import picoweb
import network
import ujson
from functions import get_temperature, get_air_humidity, get_brightness, get_soil_humidity, control
import time
from threading import Thread
import steuerung_script
from results import Results

# define variables
results = {}
results_object = Results()

# this function is used to split the post request into seperate parameters
def qs_parse(qs):
 
  # define variables
  parameters = {}
  ampersandSplit = qs.split("&")
 
  # split each parameter after the ambersand (&) symbol, then split with the equals (=) symbol
  for element in ampersandSplit:
    equalSplit = element.split("=")
    parameters[equalSplit[0]] = equalSplit[1]
 
  # return the parameters
  return parameters

# this function is used to start a webserver, which serves get/post requests
def rest_api():

  # define variables (used for getting assigned ip-address by boot.py file)
  sta_if = network.WLAN(network.STA_IF)
  ip = sta_if.ifconfig()

  # define picoweb app
  app = picoweb.WebApp(__name__)
 
  # define root route (not used)
  @app.route("/")
  def index(req, resp):
      
    reply = "ok"
    yield from picoweb.start_response(resp, content_type = "application/json")
    yield from resp.awrite(reply)

  # define /get_data route
  @app.route("/get_data")
  def index(req, resp):

    # get the sensordata from the results array
    temperature = results[0]
    air_humidity = results[1]
    brightness = results[2]
    soil_humidity = results[3]

    # build the json payload
    jsonData = {"temperature": temperature, "air_humidity": air_humidity, "brightness": brightness, "soil_humidity": soil_humidity}
    
    # define payload as a JSON string.
    encoded = ujson.dumps(jsonData)

    # return response
    yield from picoweb.start_response(resp, content_type = "application/json")
    yield from resp.awrite(encoded)

  # define /post_data route
  @app.route("/post_data")
  def query(req, resp):
      
      # fill variable queryString with the recived req.qs
      queryString = req.qs

      # fill parameters with output of qs_parse 
      parameters = qs_parse(queryString)

      # fill variable with matching parameter object
      temperature = parameters["temperature"]
      air_humidity = parameters["air_humidity"]
      soil_humidity = parameters["soil_humidity"]
      brightness = parameters["brightness"]
      
      # initalize steuerungs_script thread with posted target values
      thread_main = Thread(target=steuerung_script.main, args=[temperature, air_humidity, soil_humidity, brightness, results_object])
      
      # start steuerungs_script thread
      thread_main.start()

      # return response
      yield from picoweb.start_response(resp)
      yield from resp.awrite("Received temperature value: " + parameters["temperature"] + "\n")
      yield from resp.awrite("Received air_humidity value: " + parameters["air_humidity"] + "\n")
      yield from resp.awrite("Received soil_humidity value: " + parameters["soil_humidity"] + "\n")
      yield from resp.awrite("Received brightness value: " + parameters["brightness"])

  # start the app
  app.run(debug=True, host =ip[0])

# this function is used to obtain sensordata every 30 seconds
def collect(results):
    
    while True:  
        
        # fill array results with output of the specific sensordata function
        results[0]= get_temperature()
        results[1]= get_air_humidity()
        results[2]= get_brightness()
        results[3]= get_soil_humidity()
        
        # set collected sensordata in results object
        results_object.set_result(results)
        
        # sleep 30 seconds until checking the values again
        time.sleep(30)

# this code snippet defines, what happens if main.py is called   
if __name__ == '__main__':
  
  # initalize collect thread with empty array result as argument
  thread = Thread(target=collect, args=[results])
  
  # start collect thread
  thread.start()
  
  # getting sensordata can take up to 20 seconds, hence sleep 20 seconds
  time.sleep(20)
  
  # start rest_api function
  rest_api()


