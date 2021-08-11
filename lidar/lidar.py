
import rospy
from tf2_msgs.msg import TFMessage
import os
import time

lidar_result = [0.0,0.0,0.0]

def lidarinit():
    os.system("screen -dmS core roscore")
    print("lidar core started")
    time.sleep(7)
    os.system("screen -dmS lidar roslaunch ydlidar_ros X4.launch")
    print("lidar device started")
    time.sleep(7)
    os.system("screen -dmS mapping roslaunch hector_mapping mapping_default.launch")
    print("lidar mapping started")

def lidarcallback(data):
    myfinaldata = data.transforms[0]
    if(myfinaldata.child_frame_id == "scanmatcher_frame"):
        global lidar_result
        lidar_result[0] = myfinaldata.transform.translation.x
        lidar_result[1] = myfinaldata.transform.translation.y
        lidar_result[2] = myfinaldata.transform.rotation.z
def lidarlisten():
    try:
        global lidar_result
        lidar_result = [0.0,0.0,0.0]
        rospy.init_node('listener', anonymous=True)
        while(lidar_result[0] == 0.0):
            rospy.Subscriber('/tf', TFMessage, lidarcallback)
        return(lidar_result)

    except KeyboardInterrupt:
        lidarterminate()
        exit()

def lidarterminate():
    os.system("screen -S mapping -X quit")
    print("lidar mapping terminated")
    time.sleep(1)
    os.system("screen -S lidar -X quit")
    print("lidar device terminated")
    time.sleep(1)
    os.system("screen -S core -X quit")
    print("lidar core terminated")
