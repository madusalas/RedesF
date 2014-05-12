#!/usr/local/bin/python
import socket
import sys 
import getpass

class FTP:
  
  def __init__(self, host,port,timeout):
		
    self.connect(host,port,timeout=_GLOBAL_DEFAULT_TIMEOUT)
		self.LOGIN ()
  
	def connect(self, host, port, timeout):  
		if host != '':
			self.host = host
		if port > 0:
			self.port = port
		self.sock = socket.create_connection((self.host, self.port),timeout)
		self.file = self.sock.makefile('rb')
		return print('Success conection')
	
	def LOGIN ():
		user = input("Username [%s]: " % getpass.getuser())
    password = input("Password [%s]: " getpass.getpass())
	  print("Welcome [%s]: "%getpass.getuser())
#Transferir archivos de texto en ambos sentidos (ASCII TYPE)
#Transferir archivos binarios en ambos sentidos (IMAGE TYPE)
	def parse_pasv(self, msg): #!
        nmsg = self.get_between(msg, '(', ')')
        p = nmsg.split(',')
        return '.'.join(p[:4]), int(p[4])*256 + int(p[5])
  def recv(self):
		rec = self.sock.recv(1024)
		print(rec)
		return rec
	
	def send(self,mes=''):
		 self.sock.send(mes + ('', '\r\n')
		 print('Message send successfully')
	def relay(self, mes='', expect=False, filt=''):
		self.send(mes, True, filt)
		return self.recv(expect)  
#Listado del directorio local y remoto
	def LIST(): #Gives list files in a directory (this FTP request is the same as the ls command)
		self.PASV()
        msg = self.sock_main.relay('LIST')
#Permitir navegar el directorio local y remoto
	def CWD(path): #Changes working directory.
		self.sock_main.relay('CWD '+dname, 250)

	def CDUP ():
		self.sock_main.relay('CDUP')

#Permitir borrar, cambiar el nombre y/o atributos (CHMOD) a un archivo o directorio en el host remoto

	def RNFR(): #RENAME FROM 
	def RNTO(): #RENAME TO (RNTO)
	def DELE (self,path):	#Deletes a file.
		os.remove(path)

	def MKD (self,path):	#Makes a directory.
		self.sock_main.relay('MKD '+dname, 257)
		
	def HELP ():	#Gives help information.
	
	def think(self, thought):
        print "!!!", str(thought), '\n'
		
	def PASV (self)
		self.pasv = false
		 if self.sock_pasv:
            self.think('Checking for open socket')
            assert not self.sock_pasv.open # make sure there is no port open
		msg = self.sock_main.relay('PASV')
        newip, newport = self.handle.parse_pasv(msg)

        # make passive connection
        self.sock_pasv = mk_socket(2, newip, newport)

        return newip, newport # return the passive IP/PORT
	def QUIT ():
		raise SystemExit

if __name__ == "__main__":
	C = FTP()
	try:
		C.connect("192.100.230.21", 21)
	except socket.error:
        print("Could not connect")
	C.LOGIN()
	#Send some data to remote server
	message = ("GET / HTTP/1.1\r\n\r\n")
	C.send(message.encode('utf-8'))
