import http.server
import socketserver
from project_env.environment import Environment


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/start_process'):
            project_name = self.path.split('/start_process/')[1]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            env = Environment(project_name)
            env.build_env()
            env.run()
        else:
            super().do_GET()

class Server():
    def __init__(self, port=42069):
        self.port = port
        self.handler_object = MyHttpRequestHandler
        self.server = socketserver.TCPServer(("", self.port), self.handler_object)
        print(f"Server started on port {self.port}")

    def start_listening(self):
        self.server.serve_forever()