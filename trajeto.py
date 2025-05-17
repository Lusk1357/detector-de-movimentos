import config
from utils import calcular_similaridade as cs
import numpy as np
from time import time

class trajetoria:
    def __init__(self, alpha=0.3, delay=1.5):
        self.alpha = alpha                      # Fator de suavização
        self.delay = delay                      # Tempo de espera para iniciar o desenho
        self.tempo_inicial = None
        self.iniciou_desenho = False

        self.trajetoria_atual = config.trajetoria_atual
        self.trajetoria_padrao = config.trajetoria_padrao
        self.MAX_PONTOS = 300                   # Limite de pontos na trajetória

    def processar_mao(self, frame, resultados):
        """Processa a mão detectada, aplicando suavização e controle de delay."""
        h, w = frame.shape[:2]
        indicador_presente = False

        if resultados and resultados.multi_hand_landmarks:
            for hand_landmarks in resultados.multi_hand_landmarks:
                landmark = hand_landmarks.landmark[8]  # Ponto do dedo indicador
                x, y = landmark.x, landmark.y
                indicador_presente = True

                now = time()
                if self.tempo_inicial is None:
                    self.tempo_inicial = now
                    self.iniciou_desenho = False
                elif not self.iniciou_desenho and (now - self.tempo_inicial >= self.delay):
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

                    # Limita o tamanho da trajetória
                    if len(self.trajetoria_atual) > self.MAX_PONTOS:
                        self.trajetoria_atual.pop(0)
        else:
            self.tempo_inicial = None
            self.iniciou_desenho = False

        return frame, indicador_presente

    def salvar_trajetoria(self):
        """Salva a trajetória atual como padrão."""
        if self.trajetoria_atual:
            self.trajetoria_padrao[:] = self.trajetoria_atual[:]
            self.trajetoria_atual.clear()
            return True
        return False

    def resetar_trajetoria(self, tipo='atual'):
        """Limpa a trajetória especificada: 'atual' ou 'padrao'."""
        if tipo == 'padrao':
            self.trajetoria_padrao.clear()
        else:
            self.trajetoria_atual.clear()

    def comparar_trajetoria(self):
        """Compara a trajetória atual com a padrão e retorna a similaridade."""
        if not self.trajetoria_padrao or len(self.trajetoria_atual) < 5:
            return 0.0
        similaridade = cs(self.trajetoria_atual, self.trajetoria_padrao)
        self.resetar_trajetoria()
        return similaridade
