#SEVIDOR FTP

import socket
import os
import pickle

DATA_SIZE = 34000000 #Constante para el buffer de datos, son 200 MB de tamaño el buffer
STANDARD_SIZE = 1024

def enviar_archivo(server, address): #Función que envia el archivo pedido por el cliente
    try:
        files = os.listdir() #Obtenemos los archivos disponibles en el directorio
        mensaje = "Escriba el nombre del archivo que solicite: "
        server.sendto(mensaje.encode("utf-8"),address)
        expected_file = server.recv(STANDARD_SIZE) #Recibimos del cliente el nombre del fichero
        name_file = expected_file.decode("utf-8")
        print("["+str(address)+"] Ha solicitado el archivo: "+name_file+".\n")

        check = False

        for cont in range(0,len(files)): #Comprobamos de que el archivo se encuentre en el sistema
            if files[cont] == name_file:
                check = True
    
        if check == True:
            msg_check = "Disponible"
            server.send(msg_check.encode("utf-8"))
            file = open(name_file,"rb") #Leemos el archivo en modo binario, por si tenemos alguna imagen, etc.
            data = file.read()
            file.close()
            server.sendall(data)
            print("[V] Archivo enviado a la dirección ["+str(address)+"].\n")

        else: #En el caso de que dicho archivo no se encuentre en el sistema
            print("[X] El nombre del archivo que solicita el usuario ["+str(address)+"] no se encuentra disponible.\n")
            msg_error = "ERROR"
            server.sendto(msg_error.encode("utf-8"),address)

    except socket.error:
        error_sockets(server,address)
 
def listar_archivos(server, address): #Enviamos al usuario todos los archivos disponibles del servidor
    try:
        files = str(os.listdir())
        print("[V] La lista de archivos alojados es la siguiente: "+files[:])
        server.send(files.encode("utf-8"))

    except socket.error:
        error_sockets(server,address)

def save_file(nombre,server): #Guardamos el archivo en el servidor
    data = server.recv(DATA_SIZE)
    archivo = open(nombre, "wb")
    archivo.write(data)
    archivo.close()

def subir_archivo(server,address):
    try:
        #1. Recibimos el nombre del archivo a subir
        print("[**********] Esperamos a que el usuario nos envíe el nombre del archivo que solicita.\n")
        name = server.recv(STANDARD_SIZE)
        title = name.decode("utf-8")
        print("["+str(address)+"] solicita el archivo con nombre: "+title+".\n")
        archivos = os.listdir()

        #2. Comprobamos que dicho archivo no se encuentre alojado en el servidor
        check = True

        for cont in range(0,len(archivos)): #Comprobamos que dicho archivo exista en el directorio del servidor
            if archivos[cont] == title:
                check = False
    

        if check == False: #En el caso de que no se encuentre, le envia un mensaje de error al cliente
            msg_except = "ERROR"
            print("[X] El archivo que el usuario quiere subir al servidor ya se encuentra alojado.\n")
            server.sendto(msg_except.encode("utf-8"),address)
            op_a = server.recv(STANDARD_SIZE)
            op_ac = op_a.decode("utf-8")
            if op_ac == "S" or op_ac == "s":
                print("["+str(address)+"] Solicita actualizar el archivo.\n")
                save_file(title,server)
                print("[V] Actualización realizada con éxito.\n")
        else:
            msg_check = "CORRECTO"
            server.send(msg_check.encode("utf-8"))
            save_file(title,server)
            print("[V] Se ha subido el archivo con éxito al servidor.\n")

    except socket.error:
        error_sockets(server,address)

def eliminar_archivo(servidor,address):
    try:
        arch = os.listdir()
        data = pickle.dumps(arch) #Comprimimos la lista en bytes
        servidor.sendto(data,address)
        op_a = servidor.recv(STANDARD_SIZE) #Esperamos a la seleccion del cliente
        op = int(op_a.decode("utf-8"))
        name_f = arch[op] #Obtenemos el nombre que el cliente nos ha solicitado
        print("["+str(address)+"] Quiere eliminar el archivo: "+name_f+".\n")
        os.remove(name_f) #Eliminamos el archivo del servidor
        print("[V] Operación realizada con éxito.\n")

    except socket.error:
        error_sockets(servidor,address)

def error_sockets(servidor,address): #Mensaje de error del socket
    msg_error = "ERROR"
    servidor.sendto(msg_error.encode("utf-8"),address)

HOST = "localhost"
PORT = 1025

print("\nSERVIDOR DE LA ESI\n")

socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind((HOST,PORT)) #Conectamos el socket con el puerto

socketServer.listen(1) #Utilizaremos un cliente en este caso

print("[**********] Estableciendo conexión con el cliente\n")

server_c, addr = socketServer.accept() #Aceptamos la conexion con el cliente

try:
    print("["+str(addr)+"] Conexión establecida con el cliente.\n")

    opb = "s"

    while opb == "s" or opb == "S":  #Opciones que nos envia el cliente
        print("[******] Esperando la opción seleccionada por el usuario.\n")
        op = server_c.recv(STANDARD_SIZE)
        opc = op.decode("utf-8")
        if opc == "1":
            enviar_archivo(server_c,addr)
        elif opc == "2":
            listar_archivos(server_c,addr)
        elif opc == "3":
            subir_archivo(server_c,addr)
        elif opc == "4":
            eliminar_archivo(server_c,addr)

        op = server_c.recv(STANDARD_SIZE)
        opb = op.decode("utf-8")

except socket.error:
    error_sockets(server_c,addr)

print("[] Se ha cerrado la conexión con el usuario ["+str(addr)+"].\n")
server_c.close()