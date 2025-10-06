import socket

PORT = 5000
server = socket.socket(socket.AF_INET)
server.bind(('', PORT))
server.listen(5)
print("Escuchando en el puerto " + str(PORT))
connection, addr = server.accept()
print("Conexión correcta!")
connection.close()
server.close()
