from camera import init_camera
from trajeto import Trajetoria
from desenho import criar_fundo, desenhar_trajetoria, mostrar_texto
import config
import cv2
from time import time, sleep

# a ser removido futuramente
class FPSController:
    def __init__(self, alvo=60):
        self.alvo = alvo
        self.ultimo = time()
        self.frame_count = 0
        self.start_time = time()
        self.fps = alvo

    def atualizar(self):
        agora = time()
        delta = agora - self.ultimo
        if delta > 0:
            self.fps = 0.9 * self.fps + 0.1 * (1 / delta)
        self.ultimo = agora
        self.frame_count += 1
        return self.fps

    def esperar_proximo_frame(self):
        tempo_esperado = 1 / self.alvo
        tempo_decorrido = time() - self.ultimo
        if tempo_decorrido < tempo_esperado:
            sleep(tempo_esperado - tempo_decorrido)

def main():
    cap, capturar_frame = init_camera()
    trajeto = Trajetoria(alpha=0.3, delay_inicio=1.5)
    fps = FPSController(60)
    mensagem = {"texto": "", "tempo": 0}

    #Loop principal
    try:
        while True:
            fps.esperar_proximo_frame()
            fps_atual = fps.atualizar()

            ret, frame, resultados = capturar_frame()
            if not ret:
                continue

            # Processa a mão
            frame, indicador = trajeto.processar_mao(frame, resultados)

            # Cria fundo
            frame_exibicao = criar_fundo(frame)

            # Desenha trajetórias
            desenhar_trajetoria(frame_exibicao)

            #FPS
            mostrar_texto(frame_exibicao, f"FPS: {int(fps_atual)}", (10, 30))

            #mensagens temporárias
            if time.time() - mensagem["tempo"] < 2:
                mostrar_texto(frame_exibicao, mensagem["texto"], (10, 60))

            # Instruções
            cv2.putText(frame_exibicao, "[G]ravar [C]omparar [R]esetar [F]undo [ESC]Sair",
                        (10, frame_exibicao.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 1)

            cv2.imshow("Rastro de Mãos", frame_exibicao)

            # ESC para encerrar
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  
                break
            #Ação dos comandos do teclado
            elif key == ord('f'):
                config.mostrar_fundo_preto = not config.mostrar_fundo_preto
                mensagem = {"texto": f"Fundo: {'Preto' if config.mostrar_fundo_preto else 'Câmera'}", "tempo": time.time()}
            elif key == ord('g') and indicador:
                if trajeto.salvar_trajetoria():
                    mensagem = {"texto": "Trajetória salva!", "tempo": time.time()}
            elif key == ord('c') and indicador:
                sim = trajeto.comparar_trajetoria()
                mensagem = {"texto": f"Similaridade: {sim:.2f}%", "tempo": time.time()}
            elif key == ord('r'):
                trajeto.resetar_trajetoria()
                mensagem = {"texto": "Resetado!", "tempo": time.time()}

    #finalização e encerramento dos recursos
    finally:
        cap.stop()
        duracao = time.time() - fps.start_time
        print(f"FPS médio: {fps.frame_count / duracao:.1f}")

if __name__ == "__main__":
    main()
