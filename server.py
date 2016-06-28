import socket
import threading
import time
import string

MAX_BYTES = 65535
mylist = list()

mydict = dict()
gamedict = dict()
gamelist = list()

GameCount = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1',9521))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(5)
print('Listening at', sock.getsockname())
def server():
    while True:
         connection, addr = sock.accept()
         print('Accept a new connection', connection.getsockname(), connection.fileno())
         try:
            mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()
         except :
            pass

def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum :
            try:
                c.send(whatToSay.encode())
            except:
                pass

def tellAll(exceptNum, whatToSay):
    for c in mylist:
        try:    
            c.send(whatToSay.encode())
            time.sleep(1)
        except:
            pass
    


def game(A, B):
    if A == 'Cut' and B == 'Par' or A == 'Sto' and B == 'Cut' or A == 'Par' and B == 'Sto':
        return 0

    elif A == 'Cut' and B == 'Sto' or A == 'Sto' and B == 'Par' or A == 'Par' and B == 'Cut':
        return 1
    
    else:
        return 2 
def subThreadIn(myconnection, connNumber):

    name = myconnection.recv(1024).decode()
    # print(name)
    mydict[myconnection.fileno()] = name # maybe not
    
    global Gamecount
    
    flag = -1
    mylist.append(myconnection) #
    while True:
        try:
            recvedMsg = myconnection.recv(MAX_BYTES).decode()
            
            if recvedMsg:
                if recvedMsg[0] == '@':
                    gamedict[name] = recvedMsg[1:] #otis use  
                   # gamelist[GameCount] = name # array 0 is otis
                    gamelist.append(name)
                                      
                   # GameCount += 1

                   # gamelist[GameCount] = 'john'# array 1 is john
                 #   gamelist.append('john')
                    print(gamelist)
                #    gamedict['john'] = 'Cut'# john use 
                    
                    if len(gamedict) == 2:
                       result = game(gamedict[gamelist[0]], gamedict[gamelist[1]])
                       if result != 2:
                           
                           print(gamelist[result])
                           tellAll(connNumber, '@'+ gamelist[result])
                       else:
                           tellAll(connNumber, '@same')    
                       gamelist.pop(0)
                       gamelist.pop(0)    
                       gamedict.popitem()
                       gamedict.popitem()                         
                    #   GameCount = 0
                          
                
                else:
                    print(recvedMsg)
                    tellOthers(connNumber,recvedMsg)

            
        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            myconnection.close()
            return

if __name__ == '__main__':
        server()

