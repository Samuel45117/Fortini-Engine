"""
EXEMPLO 2: Usar Scripts Python para Controlar Objetos

Scripts são o coração da sua lógica de jogo.
Cada objeto pode ter um script que executa `update()` a cada frame.
"""

from fortini_engine.scripting.script import Script
import math


class CuboGirando(Script):
    """Script que faz um objeto girar continuamente."""
    
    def __init__(self, game_object):
        super().__init__(game_object)
        self.rotacao_speed = 1.0  # radianos por segundo
        self.tempo = 0
    
    def start(self) -> None:
        """Chamado quando o jogo começa."""
        print(f"🎬 Script iniciado para {self.api.get_name()}")
    
    def update(self, delta_time: float) -> None:
        """Chamado a cada frame."""
        self.tempo += delta_time
        
        # Fazer o objeto girar
        rotacao = self.rotacao_speed * self.tempo
        angulo = rotacao % (2 * math.pi)
        
        # Visuais de debug a cada 1 segundo
        if int(self.tempo) != int(self.tempo - delta_time):
            print(f"⏱️  {self.api.get_name()} girando... ângulo: {math.degrees(angulo):.1f}°")


class CuboMovimento(Script):
    """Script que faz um objeto se mover em padrão senoidal."""
    
    def __init__(self, game_object):
        super().__init__(game_object)
        self.velocidade = 2.0  # unidades por segundo
        self.amplitude = 2.0   # quão longe se move
        self.tempo = 0
        self.pos_inicial = self.api.get_position()
    
    def update(self, delta_time: float) -> None:
        """Chamado a cada frame."""
        self.tempo += delta_time
        
        # Movimento em padrão ondulado
        x_offset = self.amplitude * math.sin(self.tempo * self.velocidade)
        nova_x = self.pos_inicial[0] + x_offset
        
        # Atualizar posição
        self.api.transform_set_position(nova_x, self.pos_inicial[1], self.pos_inicial[2])
        
        # Debug
        if int(self.tempo) != int(self.tempo - delta_time):
            print(f"🌊 {self.api.get_name()} em movimento... X: {nova_x:.2f}")


class ControladorCenario(Script):
    """Script de controle geral da cena."""
    
    def __init__(self, game_object):
        super().__init__(game_object)
        self.contador = 0
    
    def start(self) -> None:
        """Inicializar o cenário."""
        print(f"\n{'='*50}")
        print(f"🎮 JOGO INICIADO - {self.api.get_name()}")
        print(f"{'='*50}\n")
    
    def update(self, delta_time: float) -> None:
        """Controle geral do jogo."""
        self.contador += delta_time
        
        # A cada 5 segundos, imprimir status
        if int(self.contador) % 5 == 0 and int(self.contador - delta_time) % 5 != 0:
            print(f"\n⏰ Status do jogo em {self.contador:.0f}s")
            print(f"   Objetos na cena: {self.api.get_name()}\n")


# ============================================================================
# TESTANDO OS SCRIPTS
# ============================================================================

def teste_scripts():
    """Demonstrar como usar scripts."""
    
    print("📝 TESTE DOS SCRIPTS\n")
    
    # Criar instâncias dos scripts
    cubo1 = type('GameObject', (), {'name': 'Cubo_Girando'})()
    cubo2 = type('GameObject', (), {'name': 'Cubo_Movimento'})()
    gerenciador = type('GameObject', (), {'name': 'Gerenciador'})()
    
    # Criar scripts (não vamos rodar de verdade, só demonstrar)
    script_girando = CuboGirando(cubo1)
    script_movimento = CuboMovimento(cubo2)
    script_gerenciador = ControladorCenario(gerenciador)
    
    print("✅ Scripts criados com sucesso!")
    print(f"   - {script_girando.__class__.__name__}")
    print(f"   - {script_movimento.__class__.__name__}")
    print(f"   - {script_gerenciador.__class__.__name__}")
    
    print("\nEmulando 3 frames do jogo:")
    for frame in range(3):
        delta_time = 0.016  # ~60 FPS
        print(f"\n🔄 Frame {frame + 1}:")
        
        # Chamar update dos scripts
        script_girando.update(delta_time)
        script_movimento.update(delta_time)
        if frame == 0:
            script_gerenciador.start()
        script_gerenciador.update(delta_time)


if __name__ == "__main__":
    teste_scripts()
