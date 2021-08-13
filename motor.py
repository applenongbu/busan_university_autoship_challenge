from adafruit_servokit import ServoKit                          #서보모터 드라이버를 사용하기 위해 패키지를 불러옵니다
import board                                                    #서보모터 드라이버 패키지에 종속된 패키지입니다
import busio                                                    #위와같이 서보모터 드라이버 패키지에 종속된 패키지입니다
import time                                                     #모터 제어시 delay를 주기 위해 time패키지를 불러옵니다


class Motor:
    # 초기화
    def __init__(self):
        print("Motor init")

        # i2c 통신을 젯슨 나노의 27,28번 핀으로 시작합니다
        i2c_bus0 = (busio.I2C(board.SCL_1, board.SDA_1))

        # servo_kit 에 서보모터 드라이버를 연결합니다
        self.servo_kit = ServoKit(channels=16, i2c=i2c_bus0)

        # 0번째 모터(서보모터)에 90도 각도를 주어, 서보모터가 다른 위치를 향하고 있을 때, 정면으로 향하게 합니다
        self.servo_kit.servo[0].angle = 90
        # 1번째 모터(ESC에 연결된 BLDC 모터)에 90 신호를 주어 ESC 신호를 보정합니다(2초정도 필요함)
        self.servo_kit.servo[1].angle = 90

        # 2초정도 기다립니다
        time.sleep(2)

    # servo 동작 함수
    def servo_move(self, degree):
        # 0번째 모터(서보모터)를 주어진 각도로 움직입니다
        self.servo_kit.servo[0].angle = degree

        # 에러를 방지하기 위해 0.02초 지연합니다
        time.sleep(0.02)

    # bldc 동작 함수
    def bldc_move(self, speed):
        # 1번째 모터(BLDC 모터)를 90을 기준으로 주어진 속도로 움직입니다
        self.servo_kit.servo[1].angle = speed

        # 에러를 방지하기 위해 0.02초 지연합니다
        time.sleep(0.02)

    # 종료
    def __del__(self):
        self.servo_kit.servo[0].angle = 90
        self.servo_kit.servo[1].angle = 90
