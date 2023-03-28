from server.httpserver import Server

server = Server()
server.start_listening()

# TODO
# - find a save way to close this container
# - find a proper way of sending log info to the docker container