import os
import sys
import time
import subprocess
import json
import socket
from urllib.request import urlopen
from concurrent import futures

def icmp():
    os.system('cls & mode 70, 40')
    client = input('''
 [>] Entrez une Adresse IP : ''')
    ping(client)

def lookup():
    os.system('cls & mode 70, 40')
    client = 1
    client = input(f'''
 [>] Entrez une Adresse IP : ''')
    url1 = "http://ip-api.com/json/"
    url2 = "http://extreme-ip-lookup.com/json/"
    trackedip1 = urlopen(url1 + client)
    trackedip2 = urlopen(url2 + client)
    data1 = trackedip1.read() 
    data2 = trackedip2.read()
    values1 = json.loads(data1)
    values2 = json.loads(data2)
    
    print(f''' 
 [+] IP : ''' + values1['query'])
    print(f" [+] Ville : " + values1['city'])
    print(f" [+] Pays : " + values1['country'])
    print(f" [+] Nom de la Région : " + values1['regionName'])
    print(f" [>] Région : " + values1['region'])
    print(f" [>] ISP : " + values1['isp'])
    print(f" [>] Code ZIP : " + values1['zip'])
    print(f" [>] Type d'IP : " + values2['ipType'])
    print(f" [>] ORG : " + values2['org'])
    print(f" [>] Ville : " + values2['city'])
    print(f" [>] Latitude : " + values2['lat'])
    print(f" [>] Longitude : " + values2['lon'])

    x = input('''
 [?] X pour retourner au menu : ''')
    if x == 'x':
        main()
    else:
        print(''' 
 [!] Option Invalide...''')
        time.sleep(0.5)
        lookup()

def localip():
    os.system('cls & mode 70, 12')
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    print(f'''
 [>] Nom de l'Host : {hostname}''')
    print(f" [>] Adresse IP : {ip_address}")
    
    x = input('''
 [?] X pour retourner au menu : ''')
    if x == 'x':
        main()
    else:
        print(''' 
 [!] Option Invalide''')
        time.sleep(0.5)
        localip()

def portscan():
    os.system('cls & mode 70, 30')
    client = input('''
 [>] Entrez une Adresse IP : ''')
    timeout = int(input(" [?] Temps : "))
    print("")
    scan(client, timeout)

def validip(client):
    i = 0
    valid = True
    for element in client:
        if element == '.':
            i += 1
        else:
            try:
                int(element)
            except:
                valid = False
                pass
    if not i == 3:
        valid = False
    return valid

def ping(client):
    while not validip(client):
        client = input(" [!] Invalide, veuillez réessayer : ")
    else:
        print(''' 
 [!] Ctrl + C pour Stopper
        ''')
        time.sleep(1)
        while True:
            try:
                subprocess.check_call(f"PING {client} -n 1 | FIND \"TTL=\" > NUL",shell=True)
                print(f" [>] {client} est en ligne!")
            except subprocess.CalledProcessError:
                print(f" [>] {client} est hors ligne!")
            except KeyboardInterrupt:
                icmp()

def check_port(client, port, timeout):
   TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   TCPsock.settimeout(timeout)
   try:
       TCPsock.connect((client, port))
       return(port)
   except:
       return

def scan(client, timeout):
   threadPoolSize = 500
   portsToCheck = 10000

   executor = futures.ThreadPoolExecutor(max_workers=threadPoolSize)
   checks = [
       executor.submit(check_port, client, port, timeout)
       for port in range(0, portsToCheck, 1)
   ]

   for response in futures.as_completed(checks):
       if (response.result()):
           print(" [>] En fonction du Port : {} ".format(response.result()))


def main():
    if len(sys.argv) < 2:
        os.system('cls & mode 70, 12 & title ip multi tool │ ')
        sys.stdout.write('''
        
    [1] ICMP Pinger
    [2] IP Lookup
    [3] Mon IP
    [4] Portscan
        
    ''')
    
    choice = input("[?] Option : ")
    if choice == '1':
        icmp()
    elif choice == '2':
        lookup()
    elif choice == '3':
        localip()
    elif choice == '4':
        portscan()
    else:
        print(''' 
 [!] Option Invalide ..''')
        time.sleep(0.5)
        main()

main()