from lidar import *                             #라이다 패키지를 불러옵니다
lidarinit()                                     #라이다 장치와 관련 프로그램들을 실행합니다
for i in range(10):                             #10번동안
        try:                                    
                print(lidarlisten())            #라이다가 알아낸 배의 x,y위치와 회전값을 출력합니다
        except KeyboardInterrupt:               #키보드의 ctrl+c가 눌렸을 때
                break                           #나갑니다
lidarterminate()                                #라이다 장치와 관련 프로그램들을 종료합니다

"""
주의사항! 
이 코드를 실행시켰을 때, 무한 루프를 돌리게 되면 ctrl+c를 눌러도 정지되지 않는 버그가 발견되었습니다!
가능하면 라이다 관련 코드는 빠져나올 수 없는 무한 루프를 돌리지 마세요!
"""
