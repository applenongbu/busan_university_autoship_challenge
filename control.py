import sys
import tty
import termios

from graphic import Graphic


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
        self.motor = 'motor'

        # mode1
        if mode == 1:
            print('직접 조종')

        # mode2
        elif mode == 2:
            print('mode 2')

    # 선박 주행
    def drive(self):
        # mode1
        if self.mode == 1:
            # 주행 종료까지 반복
            while True:
                # 키 입력 받기
                key = get_key()

                # 키에 따라 주행하기
                if key == 'w':
                    print('전진')
                elif key == 'a':
                    print('좌회전')
                elif key == 'd':
                    print('우회전')
                elif key == 's':
                    print('후진')

                # 수집하기
                elif key == 'c':
                    print('수집')

                # q 입력시 주행 종료
                elif key == 'q':
                    print('주행 종료')
                    break
            return False


# 키보드 입력 처리
def get_key():
    # 스트림의 파일 설명자를 숫자로 반환
    fd = sys.stdin.fileno()

    # 파일 설명자의 속성 리스트 반환
    or_attr = termios.tcgetattr(fd)

    # 문자 입력받기
    try:
        # 파일 설명자를 raw 모드로 변환
        # raw 형식은 escape 문자에 영향 받지 않고 그대로 표시
        tty.setraw(fd)

        # 1바이트 읽기
        ch = sys.stdin.read(1)

    # 입력 완료
    finally:
        # 입력을 전송 후 파일 설명자의 속성 변환
        termios.tcsetattr(fd, termios.TCSADRAIN, or_attr)

    # 입력값 반환
    return ch
