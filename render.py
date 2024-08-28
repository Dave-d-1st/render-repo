import os
import socket
from multiprocessing import Process

html="""
"""
# Function to start the socket server
def start_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 8080))
    server.bind((host, port))
    server.listen(5)

    print(f"Socket server listening on {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        client_socket.sendall(b"Hello from socket server!")
        client_socket.close()
# The WSGI callable application
def app(environ, start_response):
    print(environ)
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Socket server is ruing."]

# Start the socket server in a separate process when the module is run
if __name__ == "_main_":
    # Start the socket server in a new process
    p = Process(target=start_socket_server)
    p.start()
    
    # WSGI app callable for Gunicorn
    # Gunicorn will invoke the app function to serve HTTP requests