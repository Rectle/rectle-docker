from server.httpserver import Server
from project_env.environment import Environment

env = Environment()
env.build_env()

server = Server()
server.start_comunication()
