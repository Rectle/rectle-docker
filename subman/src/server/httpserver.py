import http.server
import socketserver
from project_env.environment import Environment


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/start_process"):
            build_id = self.path[len("/start_process") + 1 :]
            venv = Environment(build_id)
            venv.add_project_dependencies()
            venv.run()
            print("Task finished")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif self.path.startswith("/healthcheck"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            super().do_GET()


class Server:
    def __init__(self, port=8082):
        self.port = port
        self.handler_object = RequestHandler
        self.server = socketserver.TCPServer(("", self.port), self.handler_object)
        print(f"Server started on port {self.port}")

    def start_comunication(self):
        self.server.serve_forever()
