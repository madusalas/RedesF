import asyncore
import socket
import SSL

# Client Section

class Cliente(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM) #conexion C/S
        self.connect((host, port))
    connectionPhase = 1
	
    def handle_read(self): #manejador de respuestas
        print "connectionPhase =", self.connectionPhase
    if self.connectionPhase < 3: # authentication phase
            data = self.recv(1024) #espero recibir los datos con un buffer de 1024
            print 'Received:', data
         # connectionPhase = 3 when this IF loop is done
        elif self.connectionPhase == 3: # receiving data for User
            data = self.recv(1024) #recv(buffer_size)
            print 'Received data - forward to User:', data

# Connects to User
class RelayConnection(asyncore.dispatcher):
    def __init__(self, client, sock):
        asyncore.dispatcher.__init__(self)
        self.client = client
        print "connecting to %s..." % str(sock)

    def handle_connect(self):
        print "connected."
        # Allow reading once the connection on the other side is open.
        self.client.is_readable = True

    def handle_read(self):
        self.client.send(self.recv(1024))

class RelayClient(asyncore.dispatcher):
    def __init__(self, server, client, sock):
        asyncore.dispatcher.__init__(self, client)
        self.is_readable = False
        self.relay = RelayConnection(self, sock)

    def handle_read(self):
        self.relay.send(self.recv(1024))

    def handle_close(self):
        print "Closing..."
        # If the client disconnects, close the relay connection.
        self.relay.close()
        self.close()

    def readable(self):
        return self.is_readable

if __name__ == "__main__":
    # First connection 
    connectionPhase = 1
    c = Cliente('192.100.230.21', 21) 

    asyncore.loop()
