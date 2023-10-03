import requests
import socketio


# class SocketClient:
#     def __init__(self, build_id, server_url="ws://localhost:3000/private"):
#         self.secret = self.get_secret()
#         self.server_url = server_url
#         self.socket = None
#         self.build_id = build_id

#     def get_secret(self):
#         response = requests.get("http://localhost:8080")
#         return response.json()['secret']

#     def connect(self):
#         print("connecting")
#         headers = {
#             'X-Build': self.build_id,
#             'X-Token': self.secret
#         }
        
#         # log_namespace = socketio.SocketIO.define(socketio.SocketIONamespace, '/private')
#         self.socket = socketio.SocketIO("ws://localhost", 3000, headers=headers)

#         # @self.socket.on('connect')
#         # def on_connect():
#         #     print("connected successfully")

#         print(f"Build ID: {self.build_id}")
        
#         self.socket.connect()

#     def start_build(self):
#         self.send_event("build:start")

#     def send_log(self, message):
#         self.send_event("build:log", message)

#     def send_event(self, event_name, data=None):
#         self.socket.emit(event_name, data)

#     def disconnect(self):
#         self.socket.disconnect()

class SocketClient:
    def __init__(self, build_id, server_url="ws://localhost:3000"):
        self.secret = self.get_secret()
        self.server_url = server_url
        self.socket = None
        self.build_id = build_id

    def get_secret(self):
        response = requests.get("http://localhost:8080")
        return response.json()['secret']

    def connect(self):
        print("connecting")
        self.socket = socketio.Client()
        
        @self.socket.event
        def connect():
            print("connected succesfully")
        print(f"Build ID : {self.build_id}")
        headers = {
            'X-Build': self.build_id,
            'X-Token': self.secret
        }
        self.socket.connect(self.server_url, headers=headers, namespaces=['/private'])
    
    def start_build(self):
        self.send_event("build:start")

    def send_log(self, message):
        self.send_event("build:log", message)

    def finish(self):
        self.send_event("build:finish")

    def send_event(self, event_name, data=None):
        self.socket.emit(event_name, data, namespace='/private')

    def disconnect(self):
        self.socket.disconnect()