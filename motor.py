from adafruit_servokit import ServoKit                          #서보모터 드라이버를 사용하기 위해 패키지를 불러옵니다
import board                                                    #서보모터 드라이버 패키지에 종속된 패키지입니다
import busio                                                    #위와같이 서보모터 드라이버 패키지에 종속된 패키지입니다
import time                                                     #모터 제어시 delay를 주기 위해 time패키지를 불러옵니다

"""
motorinit()함수는
배에 있는 두 종류의 모터(BLDC 프로펠러, 서보모터)들을 사용하기 위해
서보모터 드라이버와 ESC(BLDC 모터 드라이버)를 초기화 시키는 코드입니다
또한 다른 위치로 가있는 서보모터를 중앙으로 정렬하기도 합니다


작동원리
서보모터 드라이버의 모터 0번에 서보모터가 연결되어있습니다
서보모터 드라이버의 모터 1번에 BLDC 모터와 연결된 ESC(드라이버)가 연결되어 있습니다

서보모터의 경우 서보모터 드라이버만 초기화 되면 바로 사용할 수 있지만
BLDC모터의 경우 처음 전원을 켰을 때 ESC에 90의 PWM 신호를 주어 초기화를 시켜 주어야 합니다
그러고 나면 이 90 신호는 중간(정지) 신호가 되고 90보다 얼마나 작느냐 크느냐에 따라
각각 정회전 속도와 역회전 속도 신호가 됩니다
"""

def motorinit():
    print("i2c connetion initalzing")
    i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))              #i2c통신을 젯슨 나노의 27,28번 핀으로 시작합니다
    global ship_servo_kit                                       #전역변수 ship_servo_kit(서보모터 드라이버 제어 관련)를 선언합니다
    ship_servo_kit = ServoKit(channels=16, i2c=i2c_bus0)        #ship_servo_kit에 서보모터 드라이버를 연결합니다
    print("i2c connection initalzing finished")
    ship_servo_kit.servo[0].angle=90                            #0번째 모터(서보모터)에 90도 각도를 주어, 서보모터가 다른 위치를 향하고 있을 때, 정면으로 향하게 합니다
    print("servo motor initalzing finished")
    print("BLDC motor calibrating")
    ship_servo_kit.servo[1].angle=90                            #1번째 모터(ESC에 연결된 BLDC 모터)에 90 신호를 주어 ESC 신호를 보정합니다(2초정도 필요함)
    time.sleep(2)                                               #2초정도 기다립니다
    print("BLDC motor calibrating finished")

"""
servomove(각도)함수는
말 그대로 서보모터를 주어진 각도로 회전시키는 함수입니다
간단히 함수를 호출하고 각도를 넣으면 되는 함수입니다
"""
    
def servomove(degree):
    global ship_servo_kit                                       #ship_servo_kit(서보모터 드라이버 제어 관련)을 이 함수에서도 사용합니다
    ship_servo_kit.servo[0].angle=degree                        #0번째 모터(서보모터)를 주어진 각도로 움직입니다
    time.sleep(0.02)                                            #에러를 방지하기 위해 0.02초 지연합니다

"""
servomove(90을 기준으로 속도)함수는
말 그대로 BLDC 모터를 주어진 속도로 회전시키는 함수입니다
90을 기준으로 작으면 정회전을 하고, 크면 역회전을 합니다
값이 얼마나 90에서 멀어지느냐에 따라서 속도가 커집니다
간단히 함수를 호출하고 속도를 넣으면 되는 함수입니다
"""    
    
def bldcmove(speed):
    global ship_servo_kit                                       #ship_servo_kit(서보모터 드라이버 제어 관련)을 이 함수에서도 사용합니다
    ship_servo_kit.servo[1].angle=speed                         #1번째 모터(BLDC 모터)를 90을 기준으로 주어진 속도로 움직입니다
    time.sleep(0.02)                                            #에러를 방지하기 위해 0.02초 지연합니다
