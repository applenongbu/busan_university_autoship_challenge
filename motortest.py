from motor import *                                     #모터 관련 패키지를 불러옵니다
import time                                             #시간 지연을 주기위해 time 패키지를 불러옵니다

motorinit()                                             #서보모터 드라이버에 연결하고 BLDC모터를 캘리브레이션 합니다
input("press enter to start")                           
while(True):                                            
    try:
        bldcmove(50)                                    #40속도만큼 전진합니다(90-50)
        a = input("input servo degrees -> ")            #입력 받은 값만큼
        servomove(int(a))                               #서보를 그각도로 움직입니다
    except KeyboardInterrupt:                           #ctrl+c가 눌렸을 때
        servomove(90)                                   #서보를 정면으로 정렬합니다
        bldcmove(90)                                    #BLDC 모터를 정지합니다
        exit()                              

