from server.httpserver import Server

server = Server()
server.start_listening()

# TODO
# - safe container turn-down
# - sending log to docker container