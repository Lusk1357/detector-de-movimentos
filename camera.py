import os
import cv2
import mediapipe as mp
import threading
from queue import Queue, Empty

class cameraController:
    def __init__(self):
        os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        
        self.cap = cv2.VideoCapture(self._get_camera_backend())
        self._setup_camera()

        self.hands = self._init_mediapipe()

        self.frame_queue = Queue(maxsize=2)
        self.running = False

    def _get_camera_backend(self):
        if os.name == 'nt':
            return cv2.CAP_DSHOW
        return cv2.CAP_V4L2 if hasattr(cv2, 'CAP_V4L2') else 0

    def _setup_camera(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    def _init_mediapipe(self):
        return mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=0 
        )
    # uso das Threds --> captura dos frames
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._capture_thread, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()
        self.cap.release()
        self.hands.close()

    #leitura e configuração dos frames
    def _capture_thread(self):
    
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)  # Espelha
                while self.frame_queue.qsize() >= 2:
                    try:
                        self.frame_queue.get_nowait()
                    except Empty:
                        pass
                self.frame_queue.put(frame)

    def get_frame(self):
        try:
            frame = self.frame_queue.get_nowait()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte para MediaPipe
            results = self.hands.process(rgb)
            return True, frame, results
        except Empty:
            return False, None, None


def init_camera():
    handler = cameraController()
    handler.start()
    return handler, handler.get_frame
