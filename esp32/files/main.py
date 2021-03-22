# main script | project: Automatisiertes Gewächshaus

import picoweb
import network
import ujson
import functions
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

        temperature = functions.get_temperature()
        air_humidity = functions.get_air_humidity()

        jsonData = {"temperature": temperature, "air_humidity": air_humidity}

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


rest_api()