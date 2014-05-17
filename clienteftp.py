#!/usr/local/bin/python
import socket
import os
from os import walk

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
path = '/'

def PRINT_LOCAL(path):
    print (dirnames)
    print (directories)
    print (filenames)
    print ('\n')
		
def CONNECTION():
    socket.connect((input("Enter FTP Address: "), 21))
    RECIEVE()

def LOGIN ():
    #user = input("Username")
    user = 'userftp'
    #password = input("Password")
    password = 'r3d3sf1s1c@s'
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
    | 8.Cambiar nombre                    | 
    | 9.Cambiar permisos                  |
    | 0.Salir                             |
    |-------------------------------------|
    Seleccione una opcion
	
    '''
    return menu

def NAVIGATE(n):
    if n == '0':
        print('you select 0')
    elif n=='1':
       PRINT_LOCAL(path)
       input('')
    elif n=='2':
        print('you select 2')
    elif n=='3':
        print('you select 3')
    elif n=='4':
        print('you select 4')
    elif n=='5':
        print('you select 5')
    elif n=='6':
        print('you select 6')
    elif n=='7':
        print('you select 7')
    elif n=='8':
        print('you select 8')
    elif n=='9':
        print('you select 9')
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
	


socket.close()

