"""
작동원리
처음에 라이다를 켤 때, lidarinit() 함수를 통해 라이다를 켰었습니다.
lidarinit() 함수 에서, 리눅스 터미널로 명령을 보내서
라이다 관련 ROS 프로그램을 백그라운드로 실행시켰었습니다.

이 때 사용되었던 프로그램이
리눅스 프로그램을 백그라운드로 실행시킬 수 있는 'screen' 이라는 프로그램입니다.
screen을 이용해 core(ros 핵심 프로그램), lidar(라이다 작동 프로그램), mapping(현재 위치 매핑 및 파악 프로그램)
이 3가지 프로그램을 백그라운드로 실행시켰었습니다.

따라서 이 3가지 프로그램을 닫을 때도, screen 이라는 프로그램을 이용하여 닫을 수 있습니다.
'screen -S 프로그램이름 -X quit'
을 사용하면 screen 으로 실행되어있는 프로그램들을 종료할 수 있습니다.

사용방법
이미 lidar.py에 이 프로그램들을 종료하는 함수인 lidarterminate()가 있고
그 함수에 이 코드의 내용들이 들어 있지만, 테스트를 해본 결과 잘 종료되지 않을 때가 가끔씩 있습니다.
예를 든다면, while(True)를 사용해서 코드를 돌리다가 lidarterminate() 함수가 제대로 작동하지 않으면
코드를 종료해도 라이다는 계속 돌아가는 현상이 발생합니다.

따라서 이 코드는, 만약 다른 코드를 종료해도 라이다가 계속 돌아간다면
라이다 관련 프로그램들을 강제로 종료 시킬 수 있는 코드입니다.
"""

import os   #리눅스 터미널에 명령을 보내기 위해 OS 모듈을 포함합니다

os.system("screen -S core -X quit")   #roscore 종료
os.system("screen -S lidar -X quit")    #ydlidar_ros X4.launch 종료
os.system("screen -S mapping -X quit")    #hector_mapping mapping_default.launch 종료
