import cv2
import numpy as np
import time
import os
import database as db
ASSETS_PATH = 'Yolo_Pre_Train_Model'
MODEL_PATH = os.path.join(ASSETS_PATH, 'yolov3.cfg')
CONFIG_PATH = os.path.join(ASSETS_PATH, 'yolov3.weights')
LABELS_PATH = os.path.join(ASSETS_PATH, 'coco.txt')
classes = []


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_detect(self):

        net = cv2.dnn.readNetFromDarknet(MODEL_PATH, CONFIG_PATH)
        with open(LABELS_PATH, "rt") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 1))
        font = cv2.FONT_HERSHEY_PLAIN
        time_now = time.time()
        start_time = time.time()
        frame_id = 0
        label = ''
        confidence = 0
        while True:
            _, frame = self.video.read()
            frame_id += 1
            height, width, channels = frame.shape

            # Detecting objects
            blob = cv2.dnn.blobFromImage(frame, 1 / 255, (320, 320), (0, 0, 0), 1, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.4)
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = colors[class_ids[i]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)
            elapses_time = time.time() - time_now
            fps = frame_id / elapses_time
            t = time.strftime('%H:%M:%S')
            cv2.putText(frame, "Time: " + str(t), (0, 480), font, 3, (0, 255, 255), 2)
            cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 3, (0, 0, 255), 3)
            

            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes(), frame, label, confidence, fps, t


