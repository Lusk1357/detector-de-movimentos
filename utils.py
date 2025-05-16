import numpy as np
import math

def calcular_similaridade(a, b, n_pontos=32, tolerancia=0.05):

    #mesma escala
    def normalizar(traj):
        traj = np.array(traj)
        min_vals = traj.min(axis=0)
        max_vals = traj.max(axis=0)
        ranges = max_vals - min_vals
        ranges[ranges == 0] = 1
        return (traj - min_vals) / ranges

    #iguala os pontos
    def interpolar(traj, n):
        traj = np.array(traj)
        if len(traj) < 2:
            return np.tile(traj[0], (n, 1)) if len(traj) == 1 else np.zeros((n, 2))
        
        dists = np.sqrt(np.sum(np.diff(traj, axis=0) ** 2, axis=1))
        cumlen = np.insert(np.cumsum(dists), 0, 0)
        total_len = cumlen[-1]

        alvo = np.linspace(0, total_len, n)
        interp_traj = np.zeros((n, 2))
        j = 0
        for i in range(n):
            while j < len(cumlen) - 2 and alvo[i] > cumlen[j + 1]:
                j += 1
            t = (alvo[i] - cumlen[j]) / (cumlen[j + 1] - cumlen[j] + 1e-8)
            interp_traj[i] = (1 - t) * traj[j] + t * traj[j + 1]
        return interp_traj

    #trajetoris vazias
    if not a or not b:
        return 0.0

    try:
        a_interp = interpolar(normalizar(a), n_pontos)
        b_interp = interpolar(normalizar(b), n_pontos)

        distancias = np.linalg.norm(a_interp - b_interp, axis=1)
        total_dist = distancias.sum()
        max_dist = n_pontos * math.sqrt(2)

        #conversão
        similaridade = max(0, 100 - (total_dist / max_dist) * 100)

        # Aplica tolerância
        if similaridade >= (100 - tolerancia * 100):
            return 100.0
        
        return round(similaridade, 2)

    except Exception as e:
        print(f"Erro ao calcular similaridade: {str(e)}")
        return 0.0
