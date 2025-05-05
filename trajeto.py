import config
from utils import calcular_similaridade  


def normalizar_trajetoria(traj):
    if not traj:
        return []  # Retorna uma lista vazia caso a trajetória esteja vazia

    xs = [p[0] for p in traj]
    ys = [p[1] for p in traj]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    largura = max_x - min_x or 1  # Evita divisão por 0
    altura = max_y - min_y or 1   # Evita divisão por 0

    return [((x - min_x) / largura, (y - min_y) / altura) for x, y in traj]



def processar_mão(frame, resultados):
    

    h, w = frame.shape[:2]
    indicador_presente = False

    if resultados and resultados.multi_hand_landmarks:
        for hand_landmarks in resultados.multi_hand_landmarks:
            # Ponto 8 é a ponta do dedo indicador
            landmark = hand_landmarks.landmark[8]
            x, y = landmark.x, landmark.y
            
            # Adiciona ponto se mover significativamente
            if not config.trajetoria_atual or (abs(config.trajetoria_atual[-1][0] - x) > 0.01 or 
                                             abs(config.trajetoria_atual[-1][1] - y) > 0.01):
                config.trajetoria_atual.append((x, y))
                indicador_presente = True

    return frame, indicador_presente

def salvar_trajetoria():
    """Salva a trajetória atual e limpa a trajetória verde"""
    if len(config.trajetoria_atual) > 10:
        config.trajetoria_padrao = config.trajetoria_atual.copy()
        config.trajetoria_atual.clear()  # Limpa a trajetória verde
        return True
    return False

def comparar_trajetoria():
    if not config.trajetoria_padrao:
        return 0.0
    if len(config.trajetoria_atual) < 10:
        return 0.0
        
    # Implementação básica de comparação
    # (substitua por sua lógica real)
    return calcular_similaridade(config.trajetoria_atual,config.trajetoria_padrao)

def resetar_trajetoria(tipo='atual'):
    if tipo == 'padrao':
        config.trajetoria_padrao.clear()
    else:
        config.trajetoria_atual.clear()