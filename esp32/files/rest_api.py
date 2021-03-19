import picoweb
import network
import ujson
import functions
import time


sta_if = network.WLAN(network.STA_IF)
ip = sta_if.ifconfig()

app = picoweb.WebApp(__name__)
 
@app.route("/")
def index(req, resp):

    temperature = functions.get_temperature()
    time.sleep(10)
    air_humidity = functions.get_air_humidity()

    jsonData = {"temperature": temperature, "air_humidity": air_humidity}

    encoded = ujson.dumps(jsonData)
 
    yield from picoweb.start_response(resp, content_type = "application/json")
    yield from resp.awrite(encoded)

@app.route("/get_data")
def index(req, resp):

    temperature = functions.get_temperature()
    air_humidity = functions.get_air_humidity()

    jsonData = {"temperature": temperature, "air_humidity": air_humidity}

    encoded = ujson.dumps(jsonData)
 
    yield from picoweb.start_response(resp, content_type = "application/json")
    yield from resp.awrite(encoded)
 
app.run(debug=True, host =ip[0])