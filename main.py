from camera import iniciar_camera
from trajeto import processar_mão, salvar_trajetoria, comparar_trajetoria, resetar_trajetoria
from desenho import criar_fundo, desenhar_trajetoria, mostrar_texto
import config
import cv2
import time

class ControladorFPS:
    def __init__(self, alvo=60):
        self.alvo = alvo
        self.ultimo = time.time()
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = alvo

    def atualizar(self):
        agora = time.time()
        delta = agora - self.ultimo
        
        # Evita divisão por zero no primeiro frame
        if delta > 0:
            self.fps = 0.9 * self.fps + 0.1 * (1 / delta)
        
        self.ultimo = agora
        self.frame_count += 1
        return self.fps

    def esperar_proximo_frame(self):
        """Controla o tempo para manter FPS estável"""
        tempo_esperado = 1 / self.alvo
        tempo_decorrido = time.time() - self.ultimo
        if tempo_decorrido < tempo_esperado:
            time.sleep(tempo_esperado - tempo_decorrido)

def main():
    cap, capturar_frame = iniciar_camera()
    fps = ControladorFPS(60)
    mensagem = {"texto": "", "tempo": 0}

    try:
        while True:
            fps.esperar_proximo_frame()
            fps_atual = fps.atualizar()

            ret, frame, resultados = capturar_frame()
            if not ret:
                continue

            # Processamento
            frame, indicador = processar_mão(frame, resultados)
            frame_exibicao = criar_fundo(frame)
            desenhar_trajetoria(frame_exibicao)

            # Interface
            mostrar_texto(frame_exibicao, f"FPS: {int(fps_atual)}", (10, 30))
            
            if time.time() - mensagem["tempo"] < 2:
                mostrar_texto(frame_exibicao, mensagem["texto"], (10, 60))

            cv2.putText(frame_exibicao, "[G]ravar [C]omparar [R]esetar [F]undo [ESC]Sair", 
                       (10, frame_exibicao.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (255, 255, 255), 1)

            # Exibição
            cv2.imshow("Rastro de Mãos", frame_exibicao)

            # Controles
            key = cv2.waitKey(1) & 0xFF
            if key == 27: break
            elif key == ord('f'):
                config.mostrar_fundo_preto = not config.mostrar_fundo_preto
                mensagem = {"texto": f"Fundo: {'Preto' if config.mostrar_fundo_preto else 'Câmera'}", "tempo": time.time()}       
            elif key == ord('g') and indicador:
                if salvar_trajetoria():
                    if salvar_trajetoria():
                        mensagem = {"texto": "Trajetória salva!", "tempo": time.time()}
                        # Força redesenho sem o traço verde
                        frame_exibicao.fill(0)
                        desenhar_trajetoria(frame_exibicao)
            elif key == ord('c') and indicador:
                mensagem = {"texto": f"Similaridade: {comparar_trajetoria()}%", "tempo": time.time()}
            elif key == ord('r'):
                resetar_trajetoria()
                mensagem = {"texto": "Resetado!", "tempo": time.time()}

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"FPS médio: {fps.frame_count / (time.time() - fps.start_time):.1f}")

if __name__ == "__main__":
    main()