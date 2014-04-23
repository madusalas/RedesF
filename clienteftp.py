import socket
import time
import getpass

LOGIN = 'userftp'
PASSW = 'r3d3sf1s1c@s'

HOST = '192.100.230.21'
PORT = 21

BUFF_SIZE = 2048

def recv_timeout(s,timeout=2):
    s.setblocking(0)
    total_data=[];data='';begin=time.time()
    while True:
        if total_data and time.time()-begin>timeout:
            break
        elif time.time()-begin>timeout*2:
            break
        try:
            data=s.recv(BUFF_SIZE)
            if data:
                 total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return ''.join(total_data)

def recv_file(s,filename,timeout=1):
    s.setblocking(0)
    somedatarecved=False;data='';begin=time.time()
    f = open(filename, 'wb')
    while True:
        if somedatarecved and time.time()-begin>timeout:
            break
        elif time.time()-begin>timeout*2:
            break
        try:
            data=s.recv(BUFF_SIZE)
            if data:
                somedatarecved = True
                f.write(data)
                f.flush()
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    f.close()

def request(s, message):
    request = message + '\r\n'
    #print request
    s.send(request)

    response = recv_timeout(s)
    #print response
    return response

 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def open_child_socket(s):
    response = request(s, 'PASV')
    if not process_response(response, 'PASV'):
        return None

    iptext = response.split(' ')[4].replace('(', '').replace(')','').split(',')
    host = '%(1)s.%(2)s.%(3)s.%(4)s' % { '1' : iptext[0], '2' : iptext[1], '3' : iptext[2], '4' : iptext[3] }
    port = int(iptext[4]) * 256 + int(iptext[5])

    return open_socket(host, port)

def process_response(response, command):
    if response == '':
        return False
    isValid = True
    for a in response.splitlines():
        if int(response[0:3]) not in responsehash[command]:
            isValid = False
             break
    return isValid

def ls(s):
    file_socket = open_child_socket(s)
    if file_socket == None:
        print 'No se pudo'
        return False

    if not process_response(request(s, 'LIST'), 'LIST'):
        print 'No se pudo'
        return False

    print recv_timeout(file_socket)

    file_socket.close()

def login(s, user, passw):
    if not process_response(request(s, 'USER ' + user), 'USER'):
        print 'No existe'
        return False
    if not process_response(request(s, 'PASS ' + passw), 'PASS'):
        print 'Contraseña erronea'
        return False
    print 'Conexion exitosa!!'
    return True

def logout(s):
    ret = True
    if not process_response(request(s, 'QUIT'), 'QUIT'):
        print 'Falló'
        ret = False
    s.close()
    print 'Desconectado'
    return ret

def cd(s, path):
    if not process_response(request(s, 'CWD ' + path), 'CWD'):
        print "No se puede ir al siguiente directorio " + path
        return False
    print 'Ok'
    return True
    
def pwd(s):
    response = request(s, 'PWD')
    if not process_response(response, 'PWD'):
        print 'Falló'
        return False
    print response[4:]
    return True

def mkd(s, dir):
    if not process_response(request(s, 'MKD ' + dir), 'MKD'):
        print "No se puede crear el directorio"
        return False
    print 'Ok'
    return True

def rmd(s, dir):
    if not process_response(request(s, 'RMD ' + dir), 'RMD'):
        print "No se puede mover el directorio"
        return False
    print 'Ok'
 return True

def upload(s, filename):
    file_stream = open_child_socket(s)
    if file_stream == None:
        print 'Falló'
        return False

    if not process_response(request(s, 'STOR ' + filename), 'STOR'):
        print"No se puede subir el archivo"
        return False

    buffer = "hola"
    f = open(filename, 'rb')
    while True:
        buffer = f.read(BUFF_SIZE)
        if buffer == "":
            break
        file_stream.send(buffer)
    f.close()
    file_stream.close()
 print recv_timeout(s)
    print 'Ok'
    return True

def download(s, filename):
    file_stream = open_child_socket(s)
    if file_stream == None:
        print 'Falló'
        return False

    if not process_response(request(s, 'RETR ' + filename), 'RETR'):
        print "No se puede descargar el achivo"
        return False

    recv_file(file_stream, filename+"_")
    file_stream.close()
    print recv_timeout(s)
    print 'Ok'
    return True

def rm(s, filename):
if not process_response(request(s, 'DELE ' + filename), 'DELE'):
        print "No se puede mover el archivo"
        return False
    print 'Ok'
    return True

def connect(host, port):
    client_socket = open_socket(HOST, PORT)

    if not process_response(recv_timeout(client_socket), 'CONN'):
        print "No se puede conectar al " + HOST + ':' + str(PORT)
        client_socket = None
    else:
        print 'Conectado al ' + HOST + ':' + str(PORT)

    return client_socket

if __name__ == '__main__':

    client_socket = None
 while True:
        args = str(raw_input()).split(' ')
        command = args[0]

        if command == 'connect':
            if args == 3:
                host = args[1]
                port = int(args[2])
                client_socket = connect(host, port)
            else:
                client_socket = connect(HOST, PORT)
            continue

        if client_socket == None:
            print'Conectate a n servidor'
            continue

        if command == 'login':
            user = str(raw_input('Usuario: '))
            passw = getpass.getpass()
            if user == '':
   login(client_socket, LOGIN, PASSW)
            else:
                login(client_socket, user, passw)
        elif command == 'pwd':
            pwd(client_socket)
        elif command == 'cd':
            cd(client_socket, args[1])
        elif command == 'ls':
            ls(client_socket)
        elif command == 'mkdir':
            mkd(client_socket, args[1])
        elif command == 'rm':
            rm(client_socket, args[1])
        elif command == 'rmd':
            rmd(client_socket, args[1])
        elif command == 'upload':
            upload(client_socket, args[1])
        elif command == 'download':
            download(client_socket, args[1])
        elif command == 'logout':
            logout(client_socket)
exit()
        else:
            print 'No existe esa operacion'
