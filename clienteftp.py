iimport socket
import time
import getpass

user = 'userftp'
PASSW = 'r3d3sf1s1c@s'

HOST = '192.100.230.21'
PORT = 21
#espacio de memoria reservada para el archivo 2048
def tiempo(s):
	timeout=1
    s.setblocking(0) #se declara el socket para que no se cierre
    Tdatos=[] #se declara una lista
    inicio=time.time() #inicia timer sin parametros
    while True: #deja abierto el socket con el bucle
        if Tdatos and time.time()-inicio>timeout: #checa si hay datos en la lista o si el incio - el tiempo actual son mayor que timeout
            break
        elif time.time()-inicio>timeout*2:
            break
        try:
            datos=s.recv(2048) 
            if datos:
                 Tdatos.append(datos)
                 inicio=time.time()
            else:
                time.sleep(0.2)
        except:
            pass
    return ''.join(Tdatos)

def recv_archivo(s,archivo):
	timeout=1
    s.setblocking(0)
    Rdatos=False #datos recibidos
    inicio=time.time()
    archivo = open(archivo, 'archivo')
    while True:
        if Rdatos and time.time()-inicio>timeout:
            break
        try:
            datos=s.recv(2048)
            if datos:
                Rdatos = True
                archivo.write(datos)
              
                inicio=time.time()
            else:
                time.sleep(1)
        except:
            pass
    archivo.close()

def peticion(s,mej):
	peticion = mej
    s.send(peticion)
    respuesta = tiempo(s)
    return respuesta
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def respuesta(response, FTPcomando):
    if response == '':
        return False
    Val = True
    for a in response.splitlines():
        if int(response[0:3]) not in responsehash[FTPcomando]:
            Val = False
             break
    return Val

def ls(s):
    socketArchivo = socket1(s)
    if socketArchivo == None:
        print 'No se pudo'
        return False

    if not respuesta(peticion(s, 'LIST'), 'LIST'):
        print 'No se pudo'
        return False

    print tiempo(socketArchivo)

    socketArchivo.close()

def login(s, user, passw):
    if not respuesta(peticion(s, 'USER ' + user), 'USER'):
        print 'No existe'
        return False
    if not respuesta(peticion(s, 'PASS ' + passw), 'PASS'):
        print 'Contraseña erronea'
        return False
    print 'Conexion exitosa!!'
    return True

def logout(s):
    ret = True
    if not respuesta(peticion(s, 'QUIT'), 'QUIT'):
        print "Falló"
        ret = False
    s.close()
    print "Desconectado"
    return ret

def cd(s, path):
    if not respuesta(peticion(s, 'CWD ' + path), 'CWD'):
        print "No se puede ir al siguiente directorio " + path
        return False
    print 'Ok'
    return True
    
def pwd(s):
    response = peticion(s, 'PWD')
    if not respuesta(response, 'PWD'):
        print 'Falló'
        return False
    print response[4:]
    return True

def mkd(s, dir):
    if not respuesta(peticion(s, 'MKD ' + dir), 'MKD'):
        print "No se puede crear el directorio"
        return False
    print 'Ok'
    return True

def rmd(s, dir):
    if not respuesta(peticion(s, 'RMD ' + dir), 'RMD'):
        print "No se puede mover el directorio"
        return False
    print 'Ok'
 return True

def upload(s, archivo):
    file_stream = socket1(s)
    if file_stream == None:
        print 'Falló'
        return False

    if not respuesta(peticion(s, 'STOR ' + archivo), 'STOR'):
        print"No se puede subir el archivo"
        return False

    buffer = "hola"
    archivo = open(archivo, 'rb')
    while True:
        buffer = archivo.read(2048)
        if buffer == "":
            break
        file_stream.send(buffer)
    archivo.close()
    file_stream.close()
 print tiempo(s)
    print 'Ok'
    return True

def download(s, archivo):
    file_stream = socket1(s)
    if file_stream == None:
        print 'Falló'
        return False
    if not respuesta(peticion(s, 'RETR ' + archivo), 'RETR'):
        print "No se puede descargar el achivo"
        return False
    recv_archivo(file_stream, archivo+"_")
    file_stream.close()
    print tiempo(s)
    print "Ok"
    return True

def rm(s, archivo):
	if not respuesta(peticion(s, 'DELE ' + archivo), 'DELE'):
        print "No se puede mover el archivo"
        return False
    print "Ok"
    return True

def connect(host, port):
    clienteFTP = socket1(HOST, PORT)
    if not respuesta(tiempo(clienteFTP), 'CONN'):
        print "No se puede conectar al " + HOST + ':' + str(PORT)
        clienteFTP = None
    else:
        print 'Conectado al ' + HOST + ':' + str(PORT)
    return clienteFTP

def main():
    
	while True:
        parametro = str(raw_input()).split(' ')
        FTPcomando = parametro[0]

        if FTPcomando == "Conectado":
            if parametro == 3:
                host = parametro[1]
                port = int(parametro[2])
                clienteFTP = connect(host, port)
            else:
                clienteFTP = connect(HOST, PORT)
            continue

        if FTPcomando == 'login':
            user = str(raw_input('Usuario: '))
            passw = getpass.getpass()
            if user == '':
				login(clienteFTP, user, PASSW)
            else:
                login(clienteFTP, user, passw)
			elif FTPcomando == 'pwd': pwd(clienteFTP)
			elif FTPcomando == 'cd': cd(clienteFTP, parametro[1])
			elif FTPcomando == 'ls': ls(clienteFTP)
			elif FTPcomando == 'mkdir': mkd(clienteFTP, parametro[1])
			elif FTPcomando == 'rm': rm(clienteFTP, parametro[1])
			elif FTPcomando == 'rmd': rmd(clienteFTP, parametro[1])
			elif FTPcomando == 'upload': upload(clienteFTP, parametro[1])
			elif FTPcomando == 'download': download(clienteFTP, parametro[1])
			elif FTPcomando == 'logout': logout(clienteFTP)
			else: print "No existe esa operacion"
