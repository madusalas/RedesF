#!/usr/local/bin/python

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dir = '/'

def PRINT_LOCAL(dir):
    for filenames in walk(dir):
                    print (filenames)
                    print ('\n')
                    break
def CONNECTION():
    port=input("Enter FTP Port: ")
    
    if port == '':
         port = 21
    else: port = port
    
    socket.connect((input("Enter FTP Address: "),port))
    RECIEVE()

def LOGIN ():
    user = input("Username: ")
    #user = 'userftp'
    password = input("Password: ")
    #password = 'r3d3sf1s1c@s'
    user='USER '+user
    password='PASS '+password
    RELAY(user)
    RELAY(password)

def RECIEVE():
    rec = socket.recv(1024)
    print(rec)
    return rec

def SEND(mes=''):
    socket.send(bytes(mes + ('\r\n'),"UTF-8"))
    print('Message send successfully')

def RELAY(mes=''):
    SEND(mes)
    return RECIEVE() 
def PASV():
	socket.send(bytes('PASV \r\n','utf-8'))
	mes=socket.recv(1024)
	mes=mes.decode('utf-8')
	m=mes.split('(')
	m=m[-1].split(')')
	parse=m[0].split(',')
	IPp='.'.join(parse[:4])
	puertop=(int(parse[4])*256+int(parse[5]))
	return(IPp,puertop)
	
	
def MENU():
    menu = '''
    |-------------------------------------|
    |             Opciones                |
    |-------------------------------------|
    | 1.Listado local                     |
    | 2.Listado remoto                    | 
    | 3.Cambiar directorio local          | 
    | 4.Cambiar directorio remoto         |
    | 5.Descargar archivos                | 
    | 6.Subir archivos                    | 
    | 7.Borrar                            |
    | 8.Hacer un directorio               | 
    | 9.Cambiar nombre                    |
    | 0.Salir                             |
    |-------------------------------------|
    Seleccione una opcion
	
    '''
    return menu

def NAVIGATE(n):
    if n == '0':
        print('you select 0')
    elif n=='1':
       PRINT_LOCAL(dir)
       input('')
    elif n=='2':
	    socket.sendall(bytes('PWD '+'\r\n','utf-8'))
	    get=socket.recv(1024) 
	    print(get)   
    elif n=='3':
            os.path = dir
            for(dirnames,filenames) in walk(dir):
                    print(dirnames)
                    print(filenames)
                    break
    elif n=='4':
	    socket.sendall(bytes('CWD '+dir+'\r\n','utf-8'))
	    get=socket.recv(1024)
	    print(get)
        
    elif n=='5':
        nfilename=input("Nombre del archivo ")
        ipup,portup = PASV()
        socketp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketp.connect((ipup,portup))
        socket.send(bytes('RETR '+nfilename+ '\r\n','utf-8'))
        aux='aux'
        file = open('index.html', 'wb')
        size= os.stat('index.html')[6]
        while aux !="":
                aux=socketp.recv(size)
                aux=aux.decode()
                file.write(aux)
        file.close()
        socketp.close()
		
    elif n=='6':
            filename=input("Nombre del archivo ")
            ipup,portup = PASV()
            socketp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketp.connect((ipup,portup))
            socket.send(bytes('STOR '+filename+ '\r\n','utf-8'))
            file=open(filename,'rb')
            opened = True
            pos = 0 
            while opened:
                    file.seek(pos)
                    pos += 1024
                    if pos >= size:
                            filepart = file.read(-1)
                            opened = False
                    else:
                            filepart = f.read(1024)
                            socketp.send(filepart)
            socketp.close()
            print(RECIEVE())
    elif n=='7':
	    filename=input("Archivo que quiere borrar")
	    socket.send(bytes('DELE '+filename+'\r\n','utf-8'))
	    get=socket.recv(1024)
	    print (get)
        
    elif n=='8':
	    socket.sendall(bytes('MKD '+'/NuevoDirectorio\r\n','utf-8'))
	    get=socket.recv(1024)
	    print(get)
       
    elif n=='9':
            filename=input("Nombre del archivo")
            change=input("Nombre nuevo")
            socket.send(bytes('RNFR '+filename+'\r\n','utf-8'))
            get=socket.recv(1024)
            print (get)
            socket.send(bytes('RNTO '+change+'\r\n','utf-8'))
            get=socket.recv(1024)
            print (get)
        
    else:
        print('Esa opcion no existe')
CONNECTION()
LOGIN()
menu = MENU()
n = ' '
while n != '0':
    os.system('clear')
    print(menu)
    n = input(' ')
    NAVIGATE(n)
