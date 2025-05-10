import os
import cv2
import mediapipe as mp

def iniciar_camera():
    # Configurações que realmente melhoram performance
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Reduz logs do TensorFlow

    # Inicialização RÁPIDA da câmera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW if os.name == 'nt' else 0)
    if not cap.isOpened():
        raise RuntimeError("Câmera não disponível")

    # Configurações ESSENCIAIS (evite muitas alterações)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Inicialização LEVE do MediaPipe
    hands = mp.solutions.hands.Hands(
        static_image_mode=False,  # Mais rápido para vídeo
        max_num_hands=1,          # Apenas 1 mão
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5
    )

    def capturar_frame():
        ret, frame = cap.read()
        if not ret:
            return False, None, None

        # Processamento MÍNIMO necessário
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return True, frame, hands.process(frame_rgb)

    return cap, capturar_frame