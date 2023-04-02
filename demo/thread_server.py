import socket
import threading


def handle_client(client):
    request = None
    while request != 'quit':
        request = client.recv(255).decode('utf8')
        response = request
        client.send(response.encode('utf8'))
    client.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 15555))
server.listen()

try:
    while True:
        client, _ = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()
except KeyboardInterrupt:
    server.close()
