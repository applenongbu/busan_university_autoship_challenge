import cv2


# 화면 제어(지도, 센서값 표시)
class Graphic:
    # 초기화
    def __init__(self, title):
        # 보여줄 화면 크기
        self.width = 400
        self.height = 300

        # 이미지 제목
        self.title = title

        # 텍스트 갯수
        self.text_num = 0

    # 화면 보여주기
    def show(self, img):
        # img 사이즈 조절
        img = cv2.resize(img, (self.width, self.height))

        # img 보여주기
        cv2.imshow(self.title, img)

    # 글자 출력
    def add_text(self, img, *text):
        # text 매개변수의 index, 내용 조회
        for i, t in enumerate(text):
            # text_num, text 개수에 따라 y축 위치 조정하여 글자 출력
            cv2.putText(img, t, (5, 30*(i+self.text_num+1)), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 200), 2)
            self.text_num += 1

    # 종료
    def __del__(self):
        cv2.destroyAllWindows()
