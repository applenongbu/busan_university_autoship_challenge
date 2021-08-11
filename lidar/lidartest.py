from lidar import *
lidarinit()
for i in range(10):
        try:
                print(lidarlisten())
        except KeyboardInterrupt:
                break
lidarterminate()

