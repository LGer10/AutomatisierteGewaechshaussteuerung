# main script | project: Automatisiertes Gewächshaus
# upip.install('picoweb')
# upip.install('pycopy-ulogging')

import picoweb
import network
import ujson
from functions import get_temperature, get_air_humidity, get_brightness, get_soil_humidity, control
import time
import steuerung_script

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

        temperature = get_temperature()
        time.sleep(5)
        air_humidity = get_air_humidity()
        brightness = get_brightness()
        soil_humidity = get_soil_humidity()

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

        steuerung_script.main(temperature, air_humidity, soil_humidity, brightness)
 
        yield from picoweb.start_response(resp)
        yield from resp.awrite("Received temperature value: " + parameters["temperature"] + "\n")
        yield from resp.awrite("Received air_humidity value: " + parameters["air_humidity"] + "\n")
        yield from resp.awrite("Received soil_humidity value: " + parameters["soil_humidity"] + "\n")
        yield from resp.awrite("Received brightness value: " + parameters["brightness"])
 
    app.run(debug=True, host =ip[0])

if __name__ == '__main__':
  rest_api()