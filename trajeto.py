import config
from utils import calcular_similaridade
import numpy as np

def processar_mão(frame, resultados):
    """Captura pontos da mão com filtro de movimento mínimo"""
    h, w = frame.shape[:2]
    indicador_presente = False

    if resultados and resultados.multi_hand_landmarks:
        for hand_landmarks in resultados.multi_hand_landmarks:
            landmark = hand_landmarks.landmark[8]  # Ponta do dedo indicador
            x, y = landmark.x, landmark.y
            
            # Filtro: só adiciona se mover >1% da tela
            if (not config.trajetoria_atual or 
                np.linalg.norm([x-config.trajetoria_atual[-1][0], 
                               y-config.trajetoria_atual[-1][1]]) > 0.001):
                config.trajetoria_atual.append((x, y))
                indicador_presente = True

    return frame, indicador_presente

def salvar_trajetoria():
    """Salva a trajetória atual (sem normalização)"""
    if config.trajetoria_atual:
        config.trajetoria_padrao = config.trajetoria_atual.copy()
        config.trajetoria_atual.clear()
        return True
    return False

def comparar_trajetoria():
    """Compara trajetórias usando a função do utils"""
    if not config.trajetoria_padrao or len(config.trajetoria_atual) < 5:
        return 0.0
    return calcular_similaridade(config.trajetoria_atual, config.trajetoria_padrao)

def resetar_trajetoria(tipo='atual'):
    """Reseta trajetórias seletivamente"""
    if tipo == 'padrao':
        config.trajetoria_padrao.clear()
    else:
        config.trajetoria_atual.clear()