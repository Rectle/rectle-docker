import http.server
import socketserver


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/finished'):
            project_name = self.path.split('/start_process/')[1]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
        if self.path.startswith('/error'):
            project_name = self.path.split('/error/')[1]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
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
    

    def wait_for_response(self):
        # TODO
        # - make waiting for responce from podman container so it is certain that it executed properly or didn't in that case mark task as undone
        self.server.timeout()