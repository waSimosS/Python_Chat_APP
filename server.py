
#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    ID=0

    while True:
        client, client_address = SERVER.accept()
        ##print("%s:%s has connected." % client_address)
        client.send(bytes("Pour connecter envoyer 'JOIN' !", "utf8"))
        join = client.recv(BUFSIZ).decode("utf8")
        while (join !="JOIN"):
            client.send(bytes("Mot clé invalide !", "utf8"))
            join = client.recv(BUFSIZ).decode("utf8")
        ID+=1    
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,ID,)).start()


def handle_client(client,ID):  # prends client socket comme argument.
    """Handles a single client connection."""

    client.send(bytes("Bonjour vous êtes connecté ! Ecrivez votre nom et faire entrer !", "utf8"))
    name = client.recv(BUFSIZ).decode("utf8")
    etats[ID]="connecté"
    Ecrire_les_etats(etats)
    print(etats)
    welcome = "Bienvenue %s! Si vous voulez quitter, tapez 'QUIT' pour sortir." % name
    client.send(bytes(welcome, "utf8"))
    msg = "{} a joint le chat et son ID est {}".format(name,ID)
    
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("QUIT", "utf8"):
            broadcast(msg, name+": ")
        else:
            etats[ID]="déconnecté"
            Ecrire_les_etats(etats)
            print(etats)
            client.send(bytes("QUIT", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s a quitté le chat." % name, "utf8"))
            break

def Ecrire_les_etats(dic):
    fout = "participant.txt"
    fo = open(fout, "w")

    for k, v in dic.items():
        fo.write(str(k) + '         '+ str(v) + '\n\n')

    fo.close()


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts le message à tous les clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}
etats={}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Attente d'une connexion...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
