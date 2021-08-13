from graphic import Graphic
from motor import Motor
from socket import *


# ################### MODE LIST ####################
# mode1 : keyboard 사용해서 직접 조종
# mode2 : ...
# mode3 : ...
# ##################################################


# 선박 조종 mode 관리
class Control:
    # 초기화
    def __init__(self, mode):
        # mode 정보 저장
        self.mode = mode

        # 모터
        self.motor = Motor()

    # 선박 주행
    def start(self):
        pass

    # 선박 주행
    def drive(self):
        pass

    # 선박 주행
    def collect(self):
        pass

    # 종료
    def __del__(self):
        pass


# mode1
class ControlMode1:
    # 초기화
    def __init__(self):
        # 모터
        self.motor = Motor()

        # 모터 기본 셋팅값
        self.speed = 15
        self.direction = 0

        # 소켓 통신 셋팅
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('', 1972))
        self.sock.listen(1)

    # 선박 주행
    def drive(self):
        conn, _ = self.sock.accept()

        while True:
            data = conn.recv(1024)
            print(data)

            if data.decode('utf-8') == "exit":
                break
            if data.decode('utf-8') == "up":
                self.direction = 1
                self.motor.bldc_move(self.direction * self.speed + 90)
            elif data.decode('utf-8') == "down":
                self.direction = -1
                self.motor.bldc_move(self.direction * self.speed + 90)
            elif data.decode('utf-8') == "left":
                self.motor.servo_move(50)
            elif data.decode('utf-8') == "right":
                self.motor.servo_move(130)
            elif data.decode('utf-8') == "keyupbldc":
                self.direction = 0
                self.motor.bldc_move(self.direction * self.speed + 90)
            elif data.decode('utf-8') == "keyupservo":
                self.motor.servo_move(90)
            if data.decode('utf-8') == "one":
                self.speed = 15
                self.motor.bldc_move(self.direction * self.speed + 90)
            elif data.decode('utf-8') == "two":
                self.speed = 25
                self.motor.bldc_move(self.direction * self.speed + 90)
            elif data.decode('utf-8') == "thr":
                self.speed = 35
                self.motor.bldc_move(self.direction * self.speed + 90)
            elif data.decode('utf-8') == "for":
                self.speed = 45
                self.motor.bldc_move(self.direction * self.speed + 90)
            elif data.decode('utf-8') == "fiv":
                self.speed = 55
                self.motor.bldc_move(self.direction * self.speed + 90)

        return False
