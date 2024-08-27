import socket
import os

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host: str = "0.0.0.0"
port: int = int(os.environ.get("PORT", 8080))
print(port)
server.bind((host, port))
print(server.getsockname())