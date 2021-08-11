import rospy                            #ros 관련 명령어들을 사용하기 위해 rospy 패키지를 불러옵니다
from tf2_msgs.msg import TFMessage      #ros에서 사용하는 통신규칙 중 tf2라는 규칙을 라이다에서 사용하기 때문에 패키지를 불러옵니다
import os                               #라이다를 작동시키키 위한 ROS 프로그램들을 실행시키고 종료하기 위해, 터미널에 명령을 보낼 필요가 있습니다. 따라서 os 패키지를 불러옵니다
import time                             #코드를 일시정지 시켜, 일정시간 delay를 주기 위해 time 패키지를 불러옵니다

lidar_result = [0.0,0.0,0.0]            #라이다에서 파악한 자신의 위치가 담길 리스트를 만듭니다. 그리고 초기화합니다

"""
lidarinit()함수는
라이다를 시작하기 위해 관련 프로그램들을 백그라운드로 실행시키는 함수입니다.
ros 관련 프로그램들을 전부 다 파이썬으로 다시 개발할 수는 없지만
파이썬을 이용하여 관련 프로그램들을 실행시키거나 종료시킬 수는 있습니다.
따라서 os 패키지를 이용하여 리눅스 터미널(배시 쉘)에 관련 프로그램들을 백그라운드로 실행하라는 명령을 보낼 수 있습니다
이 때 screen 이라는 프로그램이 사용됩니다(리눅스에 screen이 깔려 있어야 합니다 'sudo apt-get install screen')
screen은 리눅스에 사용되는 프로그램들을 백그라운드로 실행시킬 수 있게 해주는 프로그램입니다.
'screen -dmS 이름 리눅스_터미널_명령어'
이 명령어를 사용하면 정해준 이름으로, 뒤에 적은 터미널 명령어가 백그라운드로 실행됩니다.
예시로 screen -dmS hello python3 lidar.py 를 치게 되면 hello라는 이름의 새창이 생기고 거기서 lidar.py파일을 실행하는 동작을 한다고 생각하면 쉽습니다. 
"""

def lidarinit():
    os.system("screen -dmS core roscore")                                               #roscore 프로그램을 백그라운드에서 실행합니다
    print("lidar core started")
    time.sleep(7)                                                                       #roscore가 실행되어야 다음 작업이 실행되므로 잠깐 기다려줍니다
    
    os.system("screen -dmS lidar roslaunch ydlidar_ros X4.launch")                      #라이다 작동 프로그램을 백그라운드에서 실행합니다
    print("lidar device started")
    time.sleep(7)                                                                       #라이다가 움직이기까지 잠시 기다려줍니다
    
    os.system("screen -dmS mapping roslaunch hector_mapping mapping_default.launch")    #라이다를 이용해 매핑을 하고 현재 위치를 파악하는 프로그램을 백그라운드에서 실행합니다
    print("lidar mapping started")

"""
lidarcallback(라이다에서 받아온 데이터 값)함수는
통신을 통해 받아온 라이다의 수많은 데이터 중, 우리 배의 위치와 회전값만 골라내어 lidar_result 변수에 값을 넣는 함수입니다.
라이다의 수 많은 점 데이터를 그대로 받아와 가공하는 것은 너무 시간이 걸리고 복잡한 알고리즘을 필요로 합니다.
따라서 hector_mapping 이라는 ROS 프로그램을 사용하여 scanmatcher_frame 라는 주제로
우리 배의 위치를 계산하여 내보내라고 하였습니다.
이 함수는 받아온 수 많은 데이터 중에서 만약 scanmatcher_frame 라는 주제의 값이 있다면 그걸 받아와서
그중에서도 x절대위치, y절대위치, 배의 회전값을 골라내 lidar_result 변수에 넣도록 되어있습니다.
"""
    
    
def lidarcallback(data):
    myfinaldata = data.transforms[0]                                #myfinaldata변수에, 라이다에서 받아온 수 많은 정보들을 저장합니다
    if(myfinaldata.child_frame_id == "scanmatcher_frame"):          #이번에 받아온 값이 scanmatcher_frame(우리 배의 위치와 회전값) 주제가 맞다면
        global lidar_result                                         #이 함수에서 lidar_result 전역변수를 사용합니다
        lidar_result[0] = myfinaldata.transform.translation.x       #lidar_result 리스트의 0번째에, 이 배의 x 위치를 넣습니다(단위 m)
        lidar_result[1] = myfinaldata.transform.translation.y       #lidar_result 리스트의 1번째에, 이 배의 y 위치를 넣습니다(단위 m)
        lidar_result[2] = myfinaldata.transform.rotation.z          #lidar_result 리스트의 2번째에, 이 배의 회전값을 넣습니다
        
"""
lidarlisten()함수는
ROS 시스템과 통신을 시작하는 명령을 내리고,
lidarcallback()함수를 내부에서 계속 실행을 시켜서
scanmatcher_frame 주제를 받고 그 값이 가공되어 나오면 반환하는 함수입니다.
lidarcallback()함수를 한번 실행한다고 해서 바로 scanmatcher_frame 주제를 받아오는 것이 아닌
우리가 원하지 않는 주제를 받아올 수 있습니다(라이다에서는 다양한 주제의 데이터를 보내옵니다)
그래서 lidar_result 리스트에 유의미한 값이 담길 때까지 lidarcallback() 함수를 계속 실행하고
lidar_result 리스트에 담긴 결과값을 반환하는 함수가 이 함수입니다
"""
        
def lidarlisten():              
    global lidar_result                                         #lidar_result 전역변수를 사용합니다
    lidar_result = [0.0,0.0,0.0]                                #lidar_result 리스트에 담긴 쓸모없는 값을 지워줍니다
    rospy.init_node('listener', anonymous=True)                 #ROS 시스템과 통신을 시작합니다(노드를 만든다고 합니다)
    while(lidar_result[0] == 0.0):                              #lidarcallback()함수를 통해 유의미한 값이 리스트에 담겨진게 아니라면
        rospy.Subscriber('/tf', TFMessage, lidarcallback)       #계속 lidarcallback()함수를 이용하여 데이터를 받아옵니다
    return(lidar_result)                                        #lidar_result 리스트에 값이 담기면 그 리스트를 반환합니다

"""
lidarterminate()함수는
라이다 관련 프로그램들을 모두 종료하는 함수입니다.
처음에 라이다를 켤 때, lidarinit() 함수를 통해 라이다를 켰었습니다.
lidarinit() 함수 에서, 리눅스 터미널로 명령을 보내서
라이다 관련 ROS 프로그램을 백그라운드로 실행시켰었습니다.
screen을 이용해 core(ros 핵심 프로그램), lidar(라이다 작동 프로그램), mapping(현재 위치 매핑 및 파악 프로그램)
이 3가지 프로그램을 백그라운드로 실행시켰었습니다.
따라서 이 3가지 프로그램을 닫을 때도, screen 이라는 프로그램을 이용하여 닫을 수 있습니다.
'screen -S 프로그램이름 -X quit'
을 사용하면 screen 으로 실행되어있는 프로그램들을 종료할 수 있습니다.
"""    

def lidarterminate():
    os.system("screen -S mapping -X quit")          #프로그램을 역순으로 끄기 시작합니다. 위치 파악 프로그램부터 종료합니다.
    print("lidar mapping terminated")
    time.sleep(1)                                   #끄는데는 딱히 기다림이 필요없으므로 조금만 delay를 줍니다
    os.system("screen -S lidar -X quit")            #라이다 작동 프로그램을 끕니다
    print("lidar device terminated")
    time.sleep(1)                                   #또 조금 기다립니다
    os.system("screen -S core -X quit")             #ROS 핵심 프로그램을 끕니다
    print("lidar core terminated")
