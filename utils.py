import math
import numpy as np

def calcular_similaridade(a, b):
    """Calcula similaridade entre trajetórias com normalização e tratamento de erros"""
    def normalizar(traj):
        if len(traj) < 2:
            return traj
            
        traj_arr = np.array(traj)
        min_vals = traj_arr.min(axis=0)
        max_vals = traj_arr.max(axis=0)
        ranges = max_vals - min_vals
        ranges[ranges == 0] = 1  # Evita divisão por zero
        return ((traj_arr - min_vals) / ranges).tolist()

    # Verificação de entradas
    if not a or not b:
        return 0.0

    try:
        # Normalização
        a_norm = normalizar(a)
        b_norm = normalizar(b)
        
        # Ajuste para mesmo comprimento
        min_len = min(len(a_norm), len(b_norm))
        if min_len < 5:  # Mínimo de pontos para comparação válida
            return 0.0
            
        a_adj = a_norm[:min_len]
        b_adj = b_norm[:min_len]
        
        # Cálculo da distância total
        total_dist = sum(math.dist(p1, p2) for p1, p2 in zip(a_adj, b_adj))
        max_possivel = min_len * math.sqrt(2)  # Distância máxima possível (diagonal)
        
        # Similaridade (0-100%)
        similaridade = max(0, 100 - (total_dist / max_possivel) * 100)
        return round(similaridade, 2)
        
    except Exception as e:
        print(f"Erro ao calcular similaridade: {str(e)}")
        return 0.0