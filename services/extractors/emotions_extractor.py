import cv2
from fer import FER
import json


class ImageTextExtractor:
    def __init__(self, sourse_path, output_path, ap_data):
        self.sourse_p = sourse_path
        self.output_p = output_path

    def find_emotions(self):
        cap = cv2.VideoCapture('./Videos/Shahta1.mp4')
        fr_rate = cap.get(cv2.CAP_PROP_FPS)
        fr_check = int(fr_rate / 2)
        fr_num = 0

        emo_list = []

        while (cap.isOpened()):
            _, frame = cap.read()

            if not fr_num % fr_check:
                frame = cv2.resize(frame, (540, 380), fx=0, fy=0,
                                   interpolation=cv2.INTER_CUBIC)
                emo_detector = FER(mtcnn=True)
                captured_emotions = emo_detector.detect_emotions(frame)

                if captured_emotions:
                    for face in captured_emotions:
                        face['time'] = fr_num / fr_rate
                        emo_list.append(face)

                if 0xFF == ord('q'):
                    break

            fr_num += 1

        cap.release()

        with open('Try.json', 'w') as f:
            json.dump(emo_list, f)
