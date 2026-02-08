"""
EXEMPLO 5: JOGO COMPLETO - Pong Simples em Python

Um exemplo de jogo funcional usando a Fortini Engine.
Demonstra tudo junto: objetos, scripts, input, física básica.
"""

from fortini_engine.scripting.script import Script
from fortini_engine.core.input import Input
import pygame
import math


class Paddle(Script):
    """Script para controlar a raquete do jogador."""
    
    def __init__(self, game_object):
        super().__init__(game_object)
        self.velocidade = 5.0
        self.max_y = 3.0
        self.min_y = -3.0
    
    def update(self, delta_time: float) -> None:
        """Mover raquete com W/S."""
        input_mgr = Input()
        pos = self.api.get_position()
        
        # Mover para cima
        if input_mgr.is_key_pressed(pygame.K_w):
            nova_y = min(pos[1] + self.velocidade * delta_time, self.max_y)
            self.api.transform_set_position(pos[0], nova_y, pos[2])
        
        # Mover para baixo
        if input_mgr.is_key_pressed(pygame.K_s):
            nova_y = max(pos[1] - self.velocidade * delta_time, self.min_y)
            self.api.transform_set_position(pos[0], nova_y, pos[2])


class Bola(Script):
    """Script para a bola que se move e quica."""
    
    def __init__(self, game_object):
        super().__init__(game_object)
        self.velocidade_x = 2.0
        self.velocidade_y = 1.5
        self.max_x = 10.0
        self.max_y = 5.0
        self.colisoes = 0
    
    def start(self) -> None:
        print("⚽ Bola iniciada!")
    
    def update(self, delta_time: float) -> None:
        """Mover bola e detectar colisões."""
        pos = self.api.get_position()
        
        # Mover bola
        nova_x = pos[0] + self.velocidade_x * delta_time
        nova_y = pos[1] + self.velocidade_y * delta_time
        
        # Quicar nas bordas Y
        if nova_y > self.max_y or nova_y < -self.max_y:
            self.velocidade_y *= -1
            nova_y = max(-self.max_y, min(self.max_y, nova_y))
            self.colisoes += 1
        
        # Quicar nas bordas X (fim de jogo)
        if nova_x > self.max_x:
            print("❌ PERDEU! A bola saiu pela direita!")
            self.api.set_active(False)
        elif nova_x < -self.max_x:
            print("🏆 GANHOU! A bola saiu pela esquerda!")
            self.api.set_active(False)
        
        self.api.transform_set_position(nova_x, nova_y, pos[2])


class GameManager(Script):
    """Gerenciador global do jogo."""
    
    def __init__(self, game_object):
        super().__init__(game_object)
        self.tempo = 0
        self.pause = False
    
    def start(self) -> None:
        print("\n" + "="*50)
        print("   🎮 PONG - FORTINI ENGINE")
        print("="*50)
        print("\nControles:")
        print("  W  - Mover raquete para cima")
        print("  S  - Mover raquete para baixo")
        print("  P  - Pausar/Retomar")
        print("  ESC - Sair")
        print("\n" + "="*50 + "\n")
    
    def update(self, delta_time: float) -> None:
        """Controle do jogo."""
        input_mgr = Input()
        
        self.tempo += delta_time
        
        # Pausa
        if input_mgr.is_key_pressed(pygame.K_p):
            self.pause = not self.pause
            status = "PAUSADO" if self.pause else "JOGANDO"
            print(f"⏸️  {status}")
        
        # Sair
        if input_mgr.is_key_pressed(pygame.K_ESCAPE):
            print("👋 Saindo...")
        
        # Status a cada 5 segundos
        if int(self.tempo) % 5 == 0 and int(self.tempo - delta_time) % 5 != 0:
            print(f"⏱️  {int(self.tempo)}s de jogo")


# ============================================================================
# CÓDIGO PARA CRIAR ESSE JOGO
# ============================================================================

def criar_jogo_pong():
    """Código completo para criar este jogo."""
    
    codigo = '''
# No seu projeto, crie um arquivo: meu_pong.py

from fortini_engine.core.engine import GameEngine
from fortini_engine.core.game_object import GameObject
from fortini_engine.assets.manager import AssetManager
from fortini_engine.scripting.script import Script


# [Cole aqui os scripts Paddle, Bola, GameManager]


def main():
    # ✅ Criar engine
    engine = GameEngine()
    engine.initialize(width=1024, height=768, title="Pong")
    
    # ✅ Obter assets
    asset_mgr = AssetManager()
    
    # ✅ Criar cena
    
    # Raquete do jogador
    paddle = GameObject("Paddle")
    paddle.mesh = asset_mgr.get_mesh("cube")
    paddle.material = asset_mgr.get_material("default")
    paddle.transform.set_position(-9, 0, 0)
    paddle.transform.set_scale(0.5, 2.0, 0.5)
    engine.current_scene.add_object(paddle)
    
    # Attach script
    from exemplo5_jogo_pong import Paddle as PaddleScript
    paddle_script = PaddleScript(paddle)
    paddle.script = paddle_script
    paddle_script.start()
    
    # Bola
    bola = GameObject("Bola")
    bola.mesh = asset_mgr.get_mesh("sphere")
    bola.material = asset_mgr.get_material("default")
    bola.transform.set_position(0, 0, 0)
    bola.transform.set_scale(0.5, 0.5, 0.5)
    engine.current_scene.add_object(bola)
    
    # Attach script
    from exemplo5_jogo_pong import Bola as BolaScript
    bola_script = BolaScript(bola)
    bola.script = bola_script
    bola_script.start()
    
    # Game manager
    manager = GameObject("GameManager")
    engine.current_scene.add_object(manager)
    
    from exemplo5_jogo_pong import GameManager
    mgr_script = GameManager(manager)
    manager.script = mgr_script
    mgr_script.start()
    
    print(f"\\n✅ Jogo criado com {len(engine.current_scene.objects)} objetos")
    
    # ✅ Rodaria o jogo
    # engine.run()


if __name__ == "__main__":
    main()
    '''
    
    return codigo


# ============================================================================
# TESTANDO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("   EXEMPLO 5: JOGO COMPLETO - PONG")
    print("="*50 + "\n")
    
    print("🎮 Um jogo de Pong simples usa:")
    print("   ✅ Objetos (raquete e bola)")
    print("   ✅ Scripts (Paddle, Bola, GameManager)")
    print("   ✅ Input (W/S para controlar)")
    print("   ✅ Física básica (movimento, colisão)")
    print("   ✅ Lógica de jogo (pontuação, game over)")
    
    print("\n" + "-"*50)
    print("CÓDIGO PARA CRIAR ESSE JOGO:")
    print("-"*50)
    print(criar_jogo_pong())
    
    print("\n" + "="*50)
    print("✅ Entendeu como criar um jogo!")
    print("="*50)
