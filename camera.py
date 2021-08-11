import cv2
import time
import numpy as np


# 동영상 설정
FRAME_W = 800
FRAME_H = 600
FPS = 10

# YOLO 파일 위치
LABELS_FILE = './shipdata/obj.names'
CONFIG_FILE = './shipdata/yolo-ship.cfg'
WEIGHTS_FILE = './ship_weight/yolo-ship_1000.weights'

# YOLO 정확도 최소값
CONFIDENCE_THRESHOLD = 0.3


# 젯슨 나노 카메라 동작 코드
def gstreamer_pipeline(capture_width=FRAME_W, capture_height=FRAME_H, frame_rate=FPS,
                       flip_method=0, display_width=FRAME_W, display_height=FRAME_H):
    return ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! video/x-raw, format=(string)BGR ! appsink"
            % (capture_width, capture_height, frame_rate,
               flip_method, display_width, display_height))


# 카메라 제어
class Camera:
    # 초기화
    def __init__(self, yolo):
        # 카메라 연결
        self.cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

        # FPS 측정용 시간 저장 변수
        self.prev_time = 0
        self.curr_time = 0

        # yolo 사용 여부(True 일때는 yolo, False 일때는 OpenCV 사용)
        self.yolo = yolo

        # yolo 사용할 때
        if self.yolo:
            # yolo-tiny 읽어오기
            self.net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)

            # label 이름, 색상 배열 생성
            self.labels = open(LABELS_FILE).read().strip().split("\n")
            self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype=np.uint8)

            # layer name 읽어오기
            ln = self.net.getLayerNames()
            self.ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # yolo 사용하지 않을 때
        else:
            self.area_min = 10000

    # 사진 찍기
    def capture(self):
        # 카메라에서 프레임 받아오기
        _, img = self.cap.read()

        # 필요시 사진 크기 조정 후 반환     # 수정 필요
        return img

    # fps 계산
    def get_fps(self):
        # 현재 시간 저장
        self.curr_time = time.time()

        # fps 계산
        sec = self.curr_time - self.prev_time
        fps = 1 / sec

        # 현재 시간을 이전 시간으로 저장
        self.prev_time = self.curr_time

        # 반올림 후 반환
        return round(fps, 1)

    # 객체 탐지
    def detect(self):
        # 사진 찍기
        img = self.capture()

        # yolo 사용할 때
        if self.yolo:
            # 이미지 크기 저장
            h = img.shape[0]
            w = img.shape[1]

            # YOLO 사용하기 위한 blob 객체 생성
            blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (320, 320), swapRB=True, crop=False)
            self.net.setInput(blob)

            # 객체 탐지 결과
            start = time.time()
            layer_outputs = self.net.forward(self.ln)
            end = time.time()
            print("[INFO] YOLO took {:.2f} seconds".format(end - start))

            # 객체 정보를 저장할 배열 생성
            boxes = []          # 객체 테두리 좌표
            confidences = []    # 객체 정확도
            class_ids = []      # 객체 이름 id 번호

            # 결과 출력하기
            for output in layer_outputs:
                for detection in output:
                    # detection 배열은 1~4번째에 객체 테두리 좌표, 5번째에 객체일 확률(객체인지 아닌지)
                    # 6번째부터가 각각의 학습된 객체에 대한 정확도이다.

                    # 학습된 모든 객체에 대한 정확도 저장
                    scores = detection[5:]
                    # 정확도가 가장 높은 객체의 id 저장
                    class_id = np.argmax(scores)
                    # 가장 높은 정확도 저장
                    confidence = scores[class_id]

                    # 정확도에 따라 필터링
                    if confidence > CONFIDENCE_THRESHOLD:
                        # 객체 테두리 좌표 정보 저장
                        box = detection[0:4] * np.array([w, h, w, h])
                        (center_x, center_y, width, height) = box.astype("int")

                        # 중심점을 좌상단 좌표로 변경하며 테두리 배열에 저장
                        # (YOLO 좌표를 파이썬 좌표로 변환)
                        boxes.append([int(center_x - (width / 2)), int(center_y - (height / 2)), int(width), int(height)])

                        # 가장 높은 정확도와 그 객체 id 저장
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # 같은 물체에 대한 테두리 제거
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, CONFIDENCE_THRESHOLD)

            # 테두리 정보 저장할 리스트
            result = []

            # 테두리 좌표가 존재할 때
            if len(indexes) != 0:
                # 테두리 좌표를 1차원 배열로 변환
                for i in indexes.flatten():
                    # 테두리 좌표 불러오기
                    (x, y, w, h) = boxes[i][0:4]

                    # 테두리 좌표 정보 추가
                    result.append(boxes[i][0:4])

                    # 객체 이름 별로 지정된 색상 가져오기
                    color = [int(c) for c in self.colors[class_ids[i]]]

                    # 객체 정보 표시
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(self.labels[class_ids[i]], confidences[i])
                    cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # 객체 탐지 결과 반환
            return img, result

        # yolo 사용하지 않을 때
        else:
            # OpenCV 사용해서 img 보정
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)                      # hsv 이미지로 변경
            img_mask1 = cv2.inRange(img_hsv, (0, 150, 0), (20, 255, 220))       # 빨간색 영역 추출1
            img_mask2 = cv2.inRange(img_hsv, (160, 150, 0), (180, 255, 220))    # 빨간색 영역 추출2
            img_detect = img_mask1 + img_mask2                                  # 추출한 결과 더하기

            # contour 찾기
            contours, _ = cv2.findContours(img_detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # contour box 좌표 정보
            result = []

            for cnt in contours:
                # contour 영역 구하기
                area = cv2.contourArea(cnt)

                # 최소 영역 이상일 때만 반복문 실행
                if area < self.area_min:
                    continue

                # contour box 좌표 구하기
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                # contour box 그리기
                cv2.drawContours(img, [box], -1, (0, 0, 255), 2)

                # contour box 좌표 정보 추가
                result.append(box)

            # img, box 좌표 정보 반환
            return img, result

    # 종료
    def __del__(self):
        # 카메라 반환
        self.cap.release()
