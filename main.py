from control import Control


# 전반적인 작업 관리자
class Manager:
    # 초기화
    def __init__(self):
        self.control = Control(1)

    # 시작 단계(초기값 수집, 주변 정보 인식)
    def start(self):
        print('start')

    # 주행 단계(부표 피해서 주행)
    def drive(self):
        self.control.drive()

    # 수집 단계(목표물 수집하며 주행)
    def collect(self):
        print('collect')

    # 종료
    def __del__(self):
        del self.control


# 최종 실행
if __name__ == "__main__":
    # 작업 관리자 호출
    manager = Manager()

    # 시작 단계
    manager.start()

    # 주행 단계(True 반환시 수집 시작/False 반환시 작업 종료)
    while manager.drive():
        # 수집 단계
        manager.collect()

    # 종료
    del manager
