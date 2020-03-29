#!/usr/bin/python vim: set fileencoding=utf-8 :
import socket ,threading
import time
from threading import Thread, Lock
mutex1 = Lock()
mutex2 = Lock()
mutex3 = Lock()



def listprd() :
    mutex1.acquire()

    f=open("fstock.txt","r")
    mutex1.release()

    lis2=[]
    lis=[]
    li=f.readlines()
    f.close()
    for c in li : 
         lis=c.split()
         lis2+=lis[0]
    return lis2
def consult_stock(i):
   mutex1.acquire()
   f=open("fstock.txt","r")
    
   lis=[]
   li=f.readlines()
   f.close()
   mutex1.release()
   d=''
   for c in li : 
         lis=c.split()
         print lis
         if len(lis)==3:
          #continue
           print '***'
           if lis[0]==str(i):
              print 'if'
              d+=c
             
   if d=='' :
     return 'non existant'
   else :
        return d 
    
def consult_factureclt(i):
        d=''
        mutex2.acquire()
        f=open("facture.txt","r")
        
        lis=[]
        li=f.readlines()
        f.close()
        mutex2.release()
        for c in li : 
            lis=c.split()
            print lis
            if len(lis)==2:
               #continue
          
               if lis[0]==str(i):
                   # print lis[0]
                    d+=c
        if d=='' :
           return 'non existant'
        else :
              return d
def consult_histo():
         d=''
         mutex3.acquire()
         f=open("histo.txt","r")
         
         lis=[]
         li=f.readlines()
         f.close()
         mutex3.release()
         for c in li :
             d+=c 
         return d  
def achat_prd(k,i,j):
    ch=''
    c=consult_stock(i)
    if c=='non existant':
       ch= 'achat impossible'
       mutex3.acquire()
       fh=open("histo.txt",'a')
       fh.write(str(k)+'\t'+str(i)+'\t\t'+str(j)+'\t'+'echec')
       fh.close()
       mutex3.release()
    else :
         n=c.split()
   
         contenu=''
         if len(n)==3:
            if int(n[2])<j :
               ch= 'achat impossible'
               mutex3.acquire()
               fh=open("histo.txt",'a')
               fh.write(str(k)+'\t'+str(i)+'\t\t'+str(j)+'\t'+'echec')
               fh.close()
               mutex3.release()
           #mise a jour
            else:
                ch= 'achat possible'
                mutex3.acquire()
                fh=open("histo.txt",'a')
                fh.write(str(k)+'\t'+str(i)+'\t\t'+str(j)+'\t'+'succes')
                fh.close()
                mutex3.release()
                f=open("fstock.txt",'r')
                li=f.readlines()
                f.close()
                for c in li : 
                    lis=c.split()
                    #print lis
                    if len(lis)==3:
                       #continue
                       #print '****'
                       if lis[0]!=str(i):
                          contenu+=c
                          print contenu
                       else:
                           l=c.split()
                           l[2]=str(int(l[2])-j)
                           print l[2]
                           s=l[0]+'\t'+l[1]+'\t'+l[2]
                           contenu+=s+'\n'
                           #print s
                           
                mutex1.acquire()
                f=open("fstock.txt",'w')
                f.write(contenu)            # f.write(l[0]+'\t'+l[1]+'\t'+l[2])
                f.close()
                mutex1.release()
         return ch                                     
class ClientThread(threading.Thread): 
    msgClient=''
    msgClient1='' 
    def __init__(self,clientAddress,clientsocket): 
        threading.Thread.__init__(self) 
        self.connexion = clientsocket
       
        print "[+] New server socket thread started for " + str(clientsocket) + ":" + str(clientAddress)
  
   
    
             
         
    def run(self):
      
       
       while True:
                  time.sleep(1)
                  msgClient=''
  	          self.connexion.send("\nBIENVENUE \n 1:VENDEUR \n 2:CLIENT \n 3:QUITTER\n")
        	  msgClient = self.connexion.recv(1024)
		  

        	  while True:
		       
		       if  msgClient=='1': 
			    self.connexion.send(" 1:Consulter Le Stock \n 2:Consulter une facture \n 3:consulter l'historique d'une commande \n 4:Quitter\n")
			    
			    msgClient=self.connexion.recv(1024)
			    if msgClient=='1':
				    self.connexion.send("Donner la reference du produit à consulter\n")
        	                    msgClient=''
        	                    msgClient=self.connexion.recv(1024)
        	                    while msgClient=='' :
                                        self.connexion.send('')
                                        msgClient=self.connexion.recv(1024)
				    
				    self.connexion.send(consult_stock(int(msgClient)))
        	                    self.connexion.send("Retour au menu principale.. \n")
        	                    break
        	                    
			    elif msgClient=='2':
				       self.connexion.send("Donner l'identifiant du client\n")
				       msgClient=''
				       msgClient=self.connexion.recv(1024)
				       while msgClient=='' :
                                           self.connexion.send('')
                                           msgClient=self.connexion.recv(1024)
				       self.connexion.send(consult_factureclt(int(msgClient)))
				       self.connexion.send("Retour au menu principale.. \n")
        	                       break
			    elif msgClient=='3':
				       self.connexion.send(consult_histo())
				       self.connexion.send("Retour au menu principale.. \n")
        	                       break
			    elif msgClient=='4':
				  self.connexion.send("Au revoir ")
				  break 
			    else:
				    print "Choix invalide"
				    break
				     
		       elif msgClient=='2':
                               self.connexion.send("Entrer votre identifiant SVP:")
                               x=self.connexion.recv(1024)
			       self.connexion.send(" 1:Acheter produit\n 2:Quitter\n")
			 
			       msgClient=self.connexion.recv(1024)
			       if msgClient=='1':
                                    self.connexion.send("list des produits"+'\n'+str(listprd()))
				    self.connexion.send("Donner la reference du produit\n")
				    msgClient1=''
				    msgClient1=self.connexion.recv(1024)
				    while msgClient1=='':
                                        self.connexion.send()
				        msgClient1=self.connexion.recv(1024)
				    msgClient2=''   
				    self.connexion.send("Donner la quantité à acheter\n")
				    msgClient2=self.connexion.recv(1024)
				    while msgClient2=='':
                                        self.connexion.send()
				        msgClient2=self.connexion.recv(1024)
				    
				    self.connexion.send(achat_prd(x,int(msgClient1),int(msgClient2)))
				    
        	                    break
			       elif msgClient=='2':
                                        self.connexion.send("Au revoir ")
					break
			       else :
				    self.connexion.send("Choix invalide !\n")
				    
		       elif msgClient=='3':
                            self.connexion.send("Au revoir ")
			    break
		       else :
			    self.connexion.send( "Choix invalide")
			    break
			     
	
       self.connexion.send("merci pour votre visite\n")
       self.connexion.send("exit")
	
LOCALHOST=""
PORT = 8096	
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((LOCALHOST, PORT)) 
print ("waiting for clients...")
threads = [] 

while True: 
    
    server.listen(5)
    connexion , clientAddress=server.accept()
    h = ClientThread(clientAddress,connexion)
    h.start()
    threads += [h] 

    for x in threads:
         x.join()
