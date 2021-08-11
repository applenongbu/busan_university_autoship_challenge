from motor import *
import time

motorinit()
input("press enter to start")
while(True):
    try:
        bldcmove(50)
        a = input("input servo degrees -> ")
        servomove(int(a))
    except KeyboardInterrupt:
        servomove(90)
        bldcmove(90)
        exit()

