import os   #리눅스 터미널에 명령을 보내기 위해 OS 모듈을 포함합니다

os.system("screen -S core -X quit")   #roscore 종료
os.system("screen -S lidar -X quit")    #ydlidar_ros X4.launch 종료
os.system("screen -S mapping -X quit")    #hector_mapping mapping_default.launch 종료
