from lidar import *                             #라이다 패키지를 불러옵니다
lidarinit()                                     #라이다 장치와 관련 프로그램들을 실행합니다
for i in range(10):                             #10번동안
        try:                                    
                print(lidarlisten())            #라이다가 알아낸 배의 x,y위치와 회전값을 출력합니다
        except KeyboardInterrupt:               #키보드의 ctrl+c가 눌렸을 때
                break                           #나갑니다
lidarterminate()                                #라이다 장치와 관련 프로그램들을 종료합니다

