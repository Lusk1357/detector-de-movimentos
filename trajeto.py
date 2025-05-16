import config
from utils import calcular_similaridade as cs
import numpy as np
import time

#alpha(media ponderada) --> suavilização, deley --> tempo de inicio
class Trajetoria:
    def __init__(self, alpha=0.3, delay=1.5):
        self.alpha = alpha
        self.delay = delay
        self.tempo_inicial = None
        self.iniciou_desenho = False

        self.trajetoria_atual = config.trajetoria_atual
        self.trajetoria_padrao = config.trajetoria_padrao

    # detecta o dedo indicador/ aplica suavização
    def processar_mao(self, frame, resultados):
        h, w = frame.shape[:2]
        indicador_presente = False

        if resultados and resultados.multi_hand_landmarks:
            for hand_landmarks in resultados.multi_hand_landmarks:
                landmark = hand_landmarks.landmark[8]
                x, y = landmark.x, landmark.y
                indicador_presente = True

                if self.tempo_inicial is None:
                    self.tempo_inicial = time.time()
                    self.iniciou_desenho = False

                elif not self.iniciou_desenho and (time.time() - self.tempo_inicial >= self.delay_inicio):
                    self.iniciou_desenho = True

                if self.iniciou_desenho:
                    if self.trajetoria_atual:
                        x_ant, y_ant = self.trajetoria_atual[-1]
                        x_suave = self.alpha * x + (1 - self.alpha) * x_ant
                        y_suave = self.alpha * y + (1 - self.alpha) * y_ant

                        if np.linalg.norm([x_suave - x_ant, y_suave - y_ant]) > 0.001:
                            self.trajetoria_atual.append((x_suave, y_suave))
                    else:
                        self.trajetoria_atual.append((x, y))
        else:
            self.tempo_inicial = None
            self.iniciou_desenho = False

        return frame, indicador_presente

    def salvar_trajetoria(self):
        if self.trajetoria_atual:
            self.trajetoria_padrao[:] = self.trajetoria_atual[:]
            self.trajetoria_atual.clear()
            return True
        return False

    def resetar_trajetoria(self, tipo='atual'):
        if tipo == 'padrao':
            self.trajetoria_padrao.clear()
        else:
            self.trajetoria_atual.clear()

    # usa a função calcular_similaridade
    def comparar_trajetoria(self):
        if not self.trajetoria_padrao or len(self.trajetoria_atual) < 5:
            return 0.0
        similaridade = cs(self.trajetoria_atual, self.trajetoria_padrao)
        self.resetar_trajetoria()
        return similaridade
