import requests
import socketio


class SocketClient:
    def __init__(self, server_url="ws://localhost:3000/private"):
        self.secret = self.get_secret()
        self.server_url = server_url
        self.socket = None

    def get_secret(self):
        response = requests.get("http://localhost:8080")
        return response.json()['secret']

    def connect(self):
        self.socket = socketio.Client()
        
        @self.socket.event
        def connect():
            print("connected succesfully")

        self.socket.connect(self.server_url)
    
    def start_build(self):
        self.send_event("build:start")

    def send_log(self, message):
        self.send_event("build:log", message)

    def send_event(self, event_name, data=None):
        if self.socket and self.socket.connected:
            self.socket.emit(event_name, data)

    def disconnect(self):
        if self.socket and self.socket.connected:
            self.socket.disconnect()