import os
from flask import Flask, render_template ,request ,send_from_directory
from threading import Timer
# import serial
from flask_socketio import SocketIO
import time
import requests
import json
import websocket 
from flask_cors import CORS, cross_origin


# -------------------Database Setup----------------------------------------
#
# from database_setup import Base,Restaurant,MenuItem
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# Connecting date base to server
# engine=create_engine('sqlite:///restaurant.db')
# Base.metadata.bind=engine

# DBSession=sessionmaker(bind=engine)
# session =DBSession()
#
# -------------------------------------------------------------------------

app=Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# wrapping our app in SocketIO
socketio = SocketIO(app)

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "static", "dist")
#ser = serial.Serial('/dev/ttyACM0', 9600)
thread = None;
thread2 = None;
k = 0;
car_lat = 20.005450
car_lon = 77.000400
car_id = 'ass9987'
car_type = 'emergency'
car_status = 'on'
driver_id = 3
journey_id = None
ws_css = None
emergency_status = False
emergency_needed = "safe"
#----------------------------------------------------------------------------------------
#This code is for taking lat and lon from serial monitor 
# def set_interval(update_location, sec):
#     def func_wrapper():
#         set_interval(update_location, sec) 
#         update_location()  
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#     return t
class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")

class InfiniteTimer2():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")



def update_location():
    global car_lat, car_lon, thread, k
    # read_serial = ser.readline()
    # car_lat = float(read_serial[0:9])
    # car_lon = float(read_serial[10:19])
    # send_url = 'http://freegeoip.net/json'
    # r = requests.get(send_url)
    # j = json.loads(r.text)
    # car_lat = j['latitude']
    # car_lon = j['longitude']
    print(car_lat,car_lon,"          ")
    socketio.emit('location',{
        'lat': car_lat,
        'lon': car_lon,
        'car_status': car_status,
        'car_type': car_type
        }, namespace = "/socket/location")
    if k != 0:
        if k == 1:
            time.sleep(3)
            k = 2
        if car_status =='on':
            update_car_status()
            update_emrgency_status()
    #print(read_serial)
#-----------------------------------------------------------------------------------------

# This function make journey entry in django server
def register_start_journey():
    global car_lat, car_lon, journey_id
    data = {
    "jstart_lat": str(car_lat),
    "jstart_lon": str(car_lon),
    "jend_lat": str(car_lat),
    "jend_lon": str(car_lon),
    "javg_speed": "0.000000",
    "jfuel_con": "0.000000",
    "jend_status": car_status,
    "jcar_number": car_id,
    "jdriver_id": 1
    }
    # json_data = json.dumps(data)
    res = requests.post('http://544b1e41.ngrok.io/api/v1/cars/journey/', json = data)
    print(res.text)
    json_response = json.loads(res.text)
    print(json_response['id'])
    journey_id = json_response['id']

#This function modifies journey entry in django server
def register_end_journey():
    global car_lat, car_lon
    data = {
    "jend_lat": str(round(car_lat + 6,6)),
    "jend_lon": str(round(car_lon + 6,6)),
    "javg_speed": "0.5000",
    "jfuel_con": "0.5000",
    "jend_status": car_status,
    "jcar_number": car_id,
    "jdriver_id": 1
    }
    # json_data = json.dumps(data)
    res = requests.put('http://544b1e41.ngrok.io/api/v1/cars/AUBT9863/journeys/' + str(journey_id) + "/", json = data)
    print(res.text)


#This functions connect to websocket for car status update

def css_on_message(ws, message):
    json_message = json.loads(message)
    if json_message['stream'] == "status":
        socketio.emit('emergency', json_message['payload'], namespace = "/socket/location")
    if json_message['stream'] == "emergency":
        print(message)
        socketio.emit('emergency_needed', json_message['payload'], namespace = "/socket/location")

def css_on_error(ws, error):
    print(error)

def css_on_close(ws):
    print("### closed ###")

def css_on_open(ws):
    print("### Connection started ###")

def car_status_socket():
    global ws_css, k
    print("Entered in car socket")
    if k == 0:
        ws_css = websocket.WebSocketApp("ws://544b1e41.ngrok.io/status/",
            on_message = css_on_message,
            on_error = css_on_error,
            on_close = css_on_close)
        ws_css.on_open = css_on_open
        k = k + 1
        ws_css.run_forever()


def update_car_status():
    global ws_css, car_lat, car_lon,car_id,car_status
    data = {
        "car_lat": str(car_lat),
        "car_lon": str(car_lon),
        "car_speed": "0.000000",
        "car_fuel": "0.00033",
        "car_temp": "0.000000",
        "car_status": car_status,
        "car_number": car_id,
        "car_driver_id": 1
    }
    req_data = {
    "stream": "status",
    "payload": data
    }
    # print(req_data)
    ws_css.send(json.dumps(req_data))

def update_car_end_status():
    global ws_css, car_lat, car_lon,car_id,car_status
    data = {
        "car_lat": str(car_lat),
        "car_lon": str(car_lon),
        "car_speed": "0.000000",
        "car_fuel": "0.00033",
        "car_temp": "0.000000",
        "car_status": 'off',
        "car_number": car_id,
        "car_driver_id": 1
    }
    req_data = {
    "stream": "status",
    "payload": data
    }
    # print(req_data)
    ws_css.send(json.dumps(req_data))


def update_emrgency_status():
    global ws_css, car_lat, car_lon
    data = {
        "ec_start_lat": str(car_lat),
        "ec_start_lon": str(car_lon),
        "ec_end_lat": str(car_lat),
        "ec_end_lon": str(car_lon),
        "ec_current_lat": str(car_lat),
        "ec_current_lon": str(car_lon),
        "vc_end_status": emergency_needed,
        "ec_car_number": car_id,
        "ec_driver_id": driver_id,
    }
    req_data = {
    "stream": "emergency",
    "payload": data
    }
    # print(req_data)
    ws_css.send(json.dumps(req_data))

def update_emrgency_end_status():
    global ws_css, car_lat, car_lon
    data = {
        "ec_start_lat": str(car_lat),
        "ec_start_lon": str(car_lon),
        "ec_end_lat": str(car_lat),
        "ec_end_lon": str(car_lon),
        "ec_current_lat": str(car_lat),
        "ec_current_lon": str(car_lon),
        "vc_end_status": emergency_needed,
        "ec_car_number": car_id,
        "ec_driver_id": driver_id,
    }
    req_data = {
    "stream": "emergency",
    "payload": data
    }
    # print(req_data)
    ws_css.send(json.dumps(req_data))
#///////////////////////////////////////////////////////////////////////////
# Simple flask routes for front end application



@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(root, path)

@app.route('/', methods=['GET'])
def redirect_to_index():
    return send_from_directory(root, 'index.html')

@app.route('/login', methods=['GET'])
def redirect_to_login():
    # set_interval(func, 1)
    return send_from_directory(root, 'index.html')

@app.route('/api/emergency', methods=['GET','POST'])
def emergency_switch():
    global emergency_status, emergency_needed
    print("Emergency called")
    if(emergency_status):
        emergency_status = False
        emergency_needed = "safe"
        update_emrgency_end_status()
    else:
        emergency_status = True
        emergency_needed = "need"
    return "Recived signal"
#/////////////////////////////////////////////////////////////////////////////

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SocketIo routes
@socketio.on('connect', namespace='/socket/location')
def start_journey():
    register_start_journey()
    global thread, thread2
    thread = InfiniteTimer(1, update_location)
    thread2 = InfiniteTimer2(1, car_status_socket)
    thread.start()
    thread2.start()


@socketio.on('disconnect', namespace="/socket/location")
def end_journey():
    global thread, ws_css, car_status
    car_status = 'off'
    time.sleep(2)
    update_car_end_status()
    thread.cancel();
    ws_css.close();
    thread2.cancel();
    register_end_journey();
    os.system("sudo shutdown -h now")
    #@reboot /usr/bin/python /path/to/myFile.py
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__ == '__main__':
    app.debug = True
    socketio.run(app,host = '0.0.0.0', port=4000)


