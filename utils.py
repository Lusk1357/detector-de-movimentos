import math

def calcular_similaridade(a, b):
    def normalizar(traj):
        xs = [p[0] for p in traj]
        ys = [p[1] for p in traj]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        largura = max_x - min_x or 1
        altura = max_y - min_y or 1
        return [((x - min_x) / largura, (y - min_y) / altura) for x, y in traj]

    if not a or not b:
        return 0.0

    a = normalizar(a)
    b = normalizar(b)
    
    min_len = min(len(a), len(b))
    a = a[:min_len]
    b = b[:min_len]

    total = sum(math.dist(p1, p2) for p1, p2 in zip(a, b))
    max_dist = len(a) * math.sqrt(2)
    return max(0, 100 - (total / max_dist) * 100)

