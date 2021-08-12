from socket import *
from motor import *
def ship_rc_mode():
    print("-"*15,"\nplease wait until motor starting\n","-"*15)
    motorinit()
    print("-"*15,"\nmotor started!\n","-"*15)
    speed = 15
    direction = 0
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', 1972))
    serverSock.listen(1)

    connectionSock, addr = serverSock.accept()

    while(True):
        data = connectionSock.recv(1024)
        print(data)
        if(data.decode('utf-8') == "exit"):
            break

        if(data.decode('utf-8') == "up"):
            direction = 1
            bldcmove(direction * speed + 90)
        elif(data.decode('utf-8') == "down"):
            direction = - 1
            bldcmove(direction * speed + 90)
        elif(data.decode('utf-8') == "left"):
            servomove(50)
        elif(data.decode('utf-8') == "right"):
            servomove(130)
        elif(data.decode('utf-8') == "keyupbldc"):
            direction = 0
            bldcmove(direction * speed + 90)
        elif(data.decode('utf-8') == "keyupservo"):
            servomove(90)
        if(data.decode('utf-8') == "one"):
            speed = 15
            bldcmove(direction * speed + 90)
        elif(data.decode('utf-8') == "two"):
            speed = 25
            bldcmove(direction * speed + 90)
        elif(data.decode('utf-8') == "thr"):
            speed = 35
            bldcmove(direction * speed + 90)
        elif(data.decode('utf-8') == "for"):
            speed = 45
            bldcmove(direction * speed + 90)
        elif(data.decode('utf-8') == "fiv"):
            speed = 50
            bldcmove(direction * speed + 90)


