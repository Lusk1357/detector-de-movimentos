import cv2
import numpy as np
import config

def criar_fundo(frame_original):
    """Cria frame de exibição conforme configuração"""
    if config.mostrar_fundo_preto:
        fundo = np.zeros_like(frame_original)
    else:
        fundo = frame_original.copy()
    return fundo

def desenhar_trajetoria(frame):
    """Desenha primeiro a padrão (vermelha) depois a atual (verde)"""
    h, w = frame.shape[:2]
    
    # 1. Desenha a trajetória SALVA (vermelha)
    if config.trajetoria_padrao:
        for i in range(1, len(config.trajetoria_padrao)):
            pt1 = (int(config.trajetoria_padrao[i-1][0]*w), int(config.trajetoria_padrao[i-1][1]*h))
            pt2 = (int(config.trajetoria_padrao[i][0]*w), int(config.trajetoria_padrao[i][1]*h))
            cv2.line(frame, pt1, pt2, (0, 0, 255), 2)  # Vermelho
    
    # 2. Desenha a trajetória ATUAL (verde) - se existir
    if config.trajetoria_atual:
        for i in range(1, len(config.trajetoria_atual)):
            pt1 = (int(config.trajetoria_atual[i-1][0]*w), int(config.trajetoria_atual[i-1][1]*h))
            pt2 = (int(config.trajetoria_atual[i][0]*w), int(config.trajetoria_atual[i][1]*h))
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)  # Verde

def mostrar_texto(frame, texto, posicao=(10, 30)):
    """Texto sempre visível"""
    cv2.putText(frame, texto, posicao, cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, (255, 255, 255), 2)