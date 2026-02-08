"""
EXEMPLO 3: Entrada de Usuário (Keyboard & Mouse)

A engine detecta teclado e mouse automaticamente.
Use Input() para verificar controles.
"""

from fortini_engine.core.input import Input
import pygame


def exemplo_input():
    """Demonstrar sistema de entrada."""
    
    print("📌 SISTEMA DE ENTRADA\n")
    print("Fortini usa Pygame para entrada. Aqui estão as principais teclas:\n")
    
    # ============================================================
    # TECLAS DO TECLADO
    # ============================================================
    
    print("🎹 TECLADO:")
    print("  - Teclas WASD para movimento")
    print(f"    pygame.K_w = {pygame.K_w}")
    print(f"    pygame.K_a = {pygame.K_a}")
    print(f"    pygame.K_s = {pygame.K_s}")
    print(f"    pygame.K_d = {pygame.K_d}")
    
    print("\n  - Teclas especiais:")
    print(f"    pygame.K_SPACE = {pygame.K_SPACE} (espaço)")
    print(f"    pygame.K_ESCAPE = {pygame.K_ESCAPE} (escape)")
    print(f"    pygame.K_RETURN = {pygame.K_RETURN} (enter)")
    
    # ============================================================
    # MOUSE
    # ============================================================
    
    print("\n🖱️  MOUSE:")
    print("  - pygame.BUTTON_LEFT = 1 (clique esquerdo)")
    print("  - pygame.BUTTON_MIDDLE = 2 (clique meio)")
    print("  - pygame.BUTTON_RIGHT = 3 (clique direito)")
    print("  - pygame.BUTTON_WHEELUP = 4 (scroll para cima)")
    print("  - pygame.BUTTON_WHEELDOWN = 5 (scroll para baixo)")


class ControladorJogador:
    """Exemplo de como usar Input em um script de controle do jogador."""
    
    def __init__(self):
        self.posicao = [0, 0, 0]
        self.velocidade = 5.0
    
    def update(self, delta_time: float):
        """Atualizar baseado em entrada."""
        
        input_mgr = Input()
        
        # Movimento horizontal
        if input_mgr.is_key_pressed(pygame.K_w):
            self.posicao[2] -= self.velocidade * delta_time
            print(f"↑ Movendo para frente: Z={self.posicao[2]:.2f}")
        
        if input_mgr.is_key_pressed(pygame.K_s):
            self.posicao[2] += self.velocidade * delta_time
            print(f"↓ Movendo para trás: Z={self.posicao[2]:.2f}")
        
        if input_mgr.is_key_pressed(pygame.K_a):
            self.posicao[0] -= self.velocidade * delta_time
            print(f"← Movendo esquerda: X={self.posicao[0]:.2f}")
        
        if input_mgr.is_key_pressed(pygame.K_d):
            self.posicao[0] += self.velocidade * delta_time
            print(f"→ Movendo direita: X={self.posicao[0]:.2f}")
        
        # Pulo
        if input_mgr.is_key_pressed(pygame.K_SPACE):
            self.posicao[1] += self.velocidade * delta_time
            print(f"⬆️  Pulando: Y={self.posicao[1]:.2f}")
        
        # Parar
        if input_mgr.is_key_pressed(pygame.K_ESCAPE):
            print("❌ Saindo do jogo...")
            return False
        
        return True


# ============================================================
# EXEMPLO: SCRIPT COM ENTRADA
# ============================================================

def exemplo_script_com_entrada():
    """Um script típico que responde à entrada."""
    
    codigo = '''from fortini_engine.scripting.script import Script
from fortini_engine.core.input import Input
import pygame


class JogadorController(Script):
    """Controlar o jogador com teclado."""
    
    def __init__(self, game_object):
        super().__init__(game_object)
        self.velocidade = 5.0
    
    def update(self, delta_time: float) -> None:
        """Cada frame, verificar entrada."""
        
        input_mgr = Input()
        
        # Movimento
        if input_mgr.is_key_w_pressed():
            self.api.transform_translate(0, 0, -self.velocidade * delta_time)
        
        if input_mgr.is_key_s_pressed():
            self.api.transform_translate(0, 0, self.velocidade * delta_time)
        
        if input_mgr.is_key_a_pressed():
            self.api.transform_translate(-self.velocidade * delta_time, 0, 0)
        
        if input_mgr.is_key_d_pressed():
            self.api.transform_translate(self.velocidade * delta_time, 0, 0)
        
        # Pulo
        if input_mgr.is_key_space_pressed():
            self.api.transform_translate(0, self.velocidade * delta_time, 0)
        
        # Position do mouse
        mouse_x, mouse_y = input_mgr.get_mouse_position()
        
        # Clique do mouse
        if input_mgr.is_mouse_button_pressed(1):  # Botão esquerdo
            print(f"Clicou em ({mouse_x}, {mouse_y})")
'''
    
    return codigo


# ============================================================
# TESTANDO
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("   EXEMPLO 3: ENTRADA (INPUT SYSTEM)")
    print("="*50 + "\n")
    
    exemplo_input()
    
    print("\n" + "="*50)
    print("   EXEMPLO: SCRIPT COM ENTRADA")
    print("="*50)
    print(exemplo_script_com_entrada())
    
    print("\n" + "="*50)
    print("✅ Entendido como usar Input!")
    print("="*50)
