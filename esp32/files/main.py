# main script | project: Automatisiertes Gewächshaus
# upip.install('picoweb')
# upip.install('pycopy-ulogging')

import picoweb
import network
import ujson
from functions import get_temperature, get_air_humidity, get_brightness, get_soil_humidity, control
import time
from threading import Thread
import steuerung_script
from results import Results

results = {}
results_object = Results()
def qs_parse(qs):
 
  parameters = {}
  ampersandSplit = qs.split("&")
 
  for element in ampersandSplit:
    equalSplit = element.split("=")
    parameters[equalSplit[0]] = equalSplit[1]
 
  return parameters


def rest_api():

  sta_if = network.WLAN(network.STA_IF)
  ip = sta_if.ifconfig()

  app = picoweb.WebApp(__name__)
 
  @app.route("/")
  def index(req, resp):
      
    reply = "ok"
    yield from picoweb.start_response(resp, content_type = "application/json")
    yield from resp.awrite(reply)

  @app.route("/get_data")
  def index(req, resp):

    temperature = results[0]
    air_humidity = results[1]
    brightness = results[2]
    soil_humidity = results[3]

    jsonData = {"temperature": temperature, "air_humidity": air_humidity, "brightness": brightness, "soil_humidity": soil_humidity}
    
    encoded = ujson.dumps(jsonData)

    yield from picoweb.start_response(resp, content_type = "application/json")
    yield from resp.awrite(encoded)

  @app.route("/post_data")
  def query(req, resp):
      queryString = req.qs

      parameters = qs_parse(queryString)

      temperature = parameters["temperature"]
      air_humidity = parameters["air_humidity"]
      soil_humidity = parameters["soil_humidity"]
      brightness = parameters["brightness"]
      
      thread_main = Thread(target=steuerung_script.main, args=[temperature, air_humidity, soil_humidity, brightness, results_object])
      thread_main.start()

      yield from picoweb.start_response(resp)
      yield from resp.awrite("Received temperature value: " + parameters["temperature"] + "\n")
      yield from resp.awrite("Received air_humidity value: " + parameters["air_humidity"] + "\n")
      yield from resp.awrite("Received soil_humidity value: " + parameters["soil_humidity"] + "\n")
      yield from resp.awrite("Received brightness value: " + parameters["brightness"])

  app.run(debug=True, host =ip[0])

def collect(results):
    while True:  
        
        results[0]= get_temperature()
        results[1]= get_air_humidity()
        results[2]= get_brightness()
        results[3]= get_soil_humidity()
        results_object.set_result(results)
        time.sleep(300)
    


if __name__ == '__main__':
  
  thread = Thread(target=collect, args=[results])
  thread.start()
  time.sleep(20)
  rest_api()


