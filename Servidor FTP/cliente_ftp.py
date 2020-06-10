#CLIENTE

import socket
import os
import pickle

DATA_SIZE = 34000000 #Constante para el buffer de datos
STANDARD_SIZE = 1024 #Constante para el buffer para datos mas pequeños

def recibir_archivo(servidor): #Recibir un archivo del servidor
    msg_adv = servidor.recv(STANDARD_SIZE)
    print("[SERVIDOR]: "+msg_adv.decode("utf-8")+"\n")
    name = input("NOMBRE DEL ARCHIVO (NO TE OLVIDES DE LA EXTENSIÓN): ") #HAY QUE PONER LA EXTENSIÓN DEL DOCUMENTO!
    servidor.send(name.encode("utf-8"))

    check_b = servidor.recv(STANDARD_SIZE)
    check_str = check_b.decode("utf-8")

    if check_str == "ERROR":
        print("[X] Ha ocurrido un problema en el servidor de la empresa.\n")
    else:
        print("[*******] Esperando a recibir el archivo procedente del servidor.\n")
        file_from = servidor.recv(DATA_SIZE)
        file_to_receive = open(name,"wb")
        file_to_receive.write(file_from)
        print("[V] Archivo recibido con éxito.\n")
        file_to_receive.close()

def listar_nombres(servidor):
    #Nos da una lista de los archivos que se encuentran en el servidor alojados.
    print("[*******] Esperando la lista de archivos alojados en el servidor.\n")
    lista = servidor.recv(STANDARD_SIZE)
    archivos = lista.decode("utf-8")
    print("[V] Los archivos alojados en el servidor son los siguientes: "+archivos[:])

def read_file(nombre,servidor): #Lee el archivo para poder subirlo al servidor
    archivo = open(nombre, "rb")
    data = archivo.read()
    servidor.send(data) #Enviamos todo el contenido del archivo
    archivo.close()

def subir_archivo(servidor): #Subir un archivo al servidor
    files = os.listdir()
    print("Lista de archivos disponibles: ")

    for cont in range(0,len(files)): #Mostramos por pantalla todos los archivos que se encuentran dentro de nuestro directorio
        print(cont, ": "+files[cont])

    op = int(input("NÚMERO DEL ARCHIVO A SUBIR: "))

    while op < 0 or op > len(files) - 1:
        print("El numero introducido no se encuentra dentro del rango disponible.\n")
        op_ac = input("¿Desea salir de esta opción? (S/S) ")
        if op_ac == "S" or op_ac == "s":
            return
        op = int(input("NÚMERO DEL ARCHIVO A SUBIR: "))

    file_up = files[op]
    servidor.send(file_up.encode("utf-8"))

    ch_b = servidor.recv(STANDARD_SIZE) #Comprobamos que el archivo no este subido en el servidor

    if ch_b.decode("utf-8") == "ERROR":
        print("[?] El archivo que usted quiere subir ya se encuentra alojado en el servidor.\n")
        op_ac = input("¿Quiere usted actualizar el archivo? (S/s) ") #Le pregunta al usuario si quiere actualizar el archivo
        servidor.send(op_ac.encode("utf-8")) #Le enviamos una respuesta al servidor
        if op_ac == "S" or op_ac == "s":
            read_file(file_up,servidor)
            print("[V] El archivo se ha actualizado con éxito.\n")
    else:
        print("[*******] Subiendo el archivo al servidor.\n")
        read_file(file_up,servidor)
        print("[V] El archivo se ha subido con éxito al servidor.\n")

def eliminar_archivo(server): #Eliminar archivo del servidor
    print("[*******] Obteniendo lista de archivos disponibles.\n")
    arch_s = server.recv(STANDARD_SIZE)
    arch = pickle.loads(arch_s) #Cargamos la lista que ha enviado el servidor

    for cont in range(0,len(arch)): #Mostramos por pantalla los archivos alojados en el servidor
        print(cont,": "+arch[cont])

    aux = -1

    while aux<0 or aux>=len(arch):
        op = input("ARCHIVO A ELIMINAR: ")
        aux = int(op)
        if aux > 0 and aux<len(arch):
            break

    server.send(op.encode("utf-8")) #Enviamos la opcion seleccionada

HOST = "localhost"
PORT = 1025

server_c  = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creamos el socket
server_c.connect((HOST,PORT)) #Conectamos el socket con el puerto

opc_1 = "S"

while opc_1 == "s" or opc_1 == "S": 
    print("\nServidor de la empresa ESI.\n")
    print("------MENÚ DEL SISTEMA------\n")
    print("1. Recibir un archivo del servidor introduciendo un nombre.\n")
    print("2. Listar el nombre de los archivos.\n")
    print("3. Subir un archivo del ordenador al servidor de la empresa.\n")
    print("4. Eliminar archivo del servidor.\n")
    opc = input("OPCIÓN: ")

    #OPCIONES QUE NOS DA EL SERVIDOR

    if opc == "1":
        server_c.send(opc.encode("utf-8"))
        recibir_archivo(server_c)
    elif opc == "2":
        server_c.send(opc.encode("utf-8"))
        listar_nombres(server_c)
    elif opc == "3":
        server_c.send(opc.encode("utf-8"))
        subir_archivo(server_c)
    elif opc == "4":
        server_c.send(opc.encode("utf-8"))
        eliminar_archivo(server_c)
    else:
        print("La opción que usted ha introducido no está disponible.\n")

    opc_1 = input("¿Desea seguir utilizando el sistema? (s/S): ")
    server_c.send(opc_1.encode("utf-8"))

server_c.close()