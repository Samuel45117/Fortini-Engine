"""
🎮 GUIA RÁPIDO - COMO USAR FORTINI ENGINE

Um guide prático e direto para começar a fazer jogos.
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🎮 FORTINI ENGINE - GUIA DE USO RÁPIDO v1.0.0          ║
║                                                              ║
║     Tudo que você precisa saber para fazer jogos!          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝


==================== PARTE 1: INSTALAÇÃO ====================

Copie e cole isso no terminal:

    pip install -r requirements.txt
    pip install -e .

✅ Pronto! Engine instalado.


==================== PARTE 2: INICIAR EDITOR ====================

Para abrir o editor visual (UI com mouse):

    python fortini_editor.py

Ou:

    python -m fortini_engine.editor.run_editor

Você verá:
  - Uma janela com editor
  - Painel esquerdo: Hierarquia (seus objetos)
  - Painel central: Viewport (3D)
  - Painel direito: Inspector (propriedades)
  - Painel inferior: Console (logs)


==================== PARTE 3: CRIAR PRIMEIRO JOGO ====================

📋 NO EDITOR:

1. Hierarquia → Right-click → Create Cube
2. Selecione o cubo
3. No Inspector, mude Position:
   - X: 0, Y: 0, Z: 0
4. Aperte Play ▶ para testar
5. Aperte Stop ⏹ para voltar ao editor


==================== PARTE 4: USAR SCRIPTS ====================

🐍 SCRIPTS SÃO ARQUIVOS .py COM LÓGICA DO JOGO

Crie um arquivo: seu_jogo/scripts/movimento.py

---arquivo: seu_jogo/scripts/movimento.py---

from fortini_engine.scripting.script import Script


class MovimentoScript(Script):
    '''Faz um objeto se mover.'''
    
    def __init__(self, game_object):
        super().__init__(game_object)
        self.velocidade = 2.0
        self.direcao = 1
    
    def start(self):
        '''Chamado quando começa.'''
        print(f"Script iniciado para {self.api.get_name()}")
    
    def update(self, delta_time):
        '''Chamado a cada frame.'''
        movimento = self.velocidade * delta_time * self.direcao
        self.api.transform_translate(movimento, 0, 0)
        
        # Inverter direção na borda
        pos = self.api.get_position()
        if pos[0] > 5 or pos[0] < -5:
            self.direcao *= -1


---

Então no editor:
1. Crie um Object
2. Scripts → Import Scripts → Selecione movimento.py
3. Attach Script
4. Play!


==================== PARTE 5: API - COMANDOS PRINCIPAIS ====================

📍 POSIÇÃO:
    api.transform_set_position(x, y, z)     # Posição absoluta
    api.transform_translate(x, y, z)        # Movimento relativo
    pos = api.get_position()                 # Pegar posição (x, y, z)

🔄 ROTAÇÃO:
    api.transform_set_rotation(pitch, yaw, roll)  # Em radianos
    import math
    api.transform_set_rotation(0, math.pi/4, 0)   # 45 graus em Y

📏 ESCALA:
    api.transform_set_scale(x, y, z)       # Tamanho
    api.transform_set_scale(2, 2, 2)       # 2x maior
    scale = api.get_scale()

👁️ VISIBILIDADE:
    api.set_active(True)                    # Mostrar
    api.set_active(False)                   # Esconder

📛 NOME:
    nome = api.get_name()


==================== PARTE 6: INPUT (TECLADO E MOUSE) ====================

⌨️ EM UM SCRIPT:

from fortini_engine.core.input import Input
import pygame


class ControladorScript(Script):
    def update(self, delta_time):
        input_mgr = Input()
        
        # Teclas WASD
        if input_mgr.is_key_w_pressed():
            print("W pressionado")
            self.api.transform_translate(0, 0, -1 * delta_time)
        
        if input_mgr.is_key_a_pressed():
            print("A pressionado")
        
        if input_mgr.is_key_s_pressed():
            print("S pressionado")
        
        if input_mgr.is_key_d_pressed():
            print("D pressionado")
        
        # Espaço
        if input_mgr.is_key_space_pressed():
            print("SPACE!")
        
        # Mouse
        x, y = input_mgr.get_mouse_position()
        
        if input_mgr.is_mouse_button_pressed(1):  # Botão esquerdo
            print(f"Clicou em {x}, {y}")


==================== PARTE 7: ESTRUTURA DO PROJETO ====================

📁 Seu Projeto Fica Em:

~/Fortini Documents/Projects/MeuJogo/

├── scenes/          ← Cenas do jogo
├── assets/          ← Modelos 3D
├── scripts/         ← Seus scripts Python
├── settings/        ← Configuração
└── project.json     ← Metadados


==================== PARTE 8: OBJETOS E HIERARQUIA ====================

🏗️ RELAÇÃO ENTRE OBJETOS:

No editor, arraste um objeto para outro para criar Pai/Filho:

    Pai
    └── Filho (segue o pai)
        ├── Neto
        └── Neto2

No código:
    parent.add_child(child)  # child agora é filho de parent
    parent.remove_child(child)

Quando move pai, filhos seguem!


==================== PARTE 9: MATERIAIS E CORES ====================

🎨 EM UM SCRIPT:

from fortini_engine.assets.manager import Material, AssetManager


class CustomScript(Script):
    def start(self):
        # Criar material vermelho
        mat = Material("Vermelho")
        mat.color = [1.0, 0.0, 0.0, 1.0]  # R, G, B, A
        
        # Criar objeto com material
        obj = GameObject("MeuCubo")
        obj.mesh = AssetManager().get_mesh("cube")
        obj.material = mat
        obj.transform.set_position(0, 0, 0)


==================== PARTE 10: EXEMPLO COMPLETO ====================

💻 CÓDIGO PARA UM JOGO SIMPLES:

---arquivo: seu_script.py---

from fortini_engine.scripting.script import Script
from fortini_engine.core.input import Input
import pygame
import math


class JogadorController(Script):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.velocidade = 5.0
        self.tempo = 0
    
    def update(self, delta_time):
        # Movimento
        input_mgr = Input()
        
        if input_mgr.is_key_w_pressed():
            self.api.transform_translate(0, 0, -self.velocidade * delta_time)
        
        if input_mgr.is_key_a_pressed():
            self.api.transform_translate(-self.velocidade * delta_time, 0, 0)
        
        if input_mgr.is_key_s_pressed():
            self.api.transform_translate(0, 0, self.velocidade * delta_time)
        
        if input_mgr.is_key_d_pressed():
            self.api.transform_translate(self.velocidade * delta_time, 0, 0)
        
        # Pulo com espaço
        if input_mgr.is_key_space_pressed():
            self.api.transform_translate(0, 1 * delta_time, 0)
        
        # Debug - mostrar posição
        self.tempo += delta_time
        if int(self.tempo) % 2 == 0 and int(self.tempo - delta_time) % 2 != 0:
            pos = self.api.get_position()
            print(f"Posição: {pos}")


---

No editor:
1. Create Cube "Jogador"
2. Attach JogadorController script
3. Play!
4. Controle com WASD + SPACE


==================== ATALHOS DO EDITOR ====================

🖥️ VIEWPORT (3D view):
    - Clique MEIO + Drag = Rotacionar câmera
    - SCROLL = Zoom
    - Right-click = Menu

📋 GERAL:
    - Play ▶ = Testar jogo (rodas)
    - Stop ⏹ = Voltar ao editor
    - Ctrl+S = Salvar projeto


==================== TROUBLESHOOTING ====================

❓ "Nenhuma janela abre"
   → Cert ificado que tem OpenGL instalado
   → Em Linux: sudo apt-get install libgl1

❓ "Script não funciona"
   → Verifique o Console para erros
   → Certifique que `class Script` está definida

❓ "Objeto não se move"
   → Verifique a scale (tamanho) - pode estar 0
   → Verifique a posição - pode estar fora da câmera

❓ "Câmera preta"
   → Afaste mais a câmera (Z+)
   → Aumente FOV (Field of View)


==================== PRÓXIMOS PASSOS ====================

Agora você sabe:
  ✅ Como instalar a engine
  ✅ Como abrir o editor
  ✅ Como criar objetos
  ✅ Como escrever scripts
  ✅ Como usar input
  ✅ Como compilar e exportar

PRÓXIMAS IDEIAS DE JOGOS:
  1. Pong - 2 palhetas, 1 bola
  2. Space Shooter - nave que atira
  3. Plataforma - pular entre plataformas
  4. Puzzle - mover cubos para posições

RECURSOS:
  📖 README.md - Documentação completa
  🏗️ ARCHITECTURE.md - Como a engine funciona
  📁 examples/ - Exemplos práticos
  💬 GitHub Issues - Ajuda da comunidade


==================== DÚVIDAS? ====================

Todos os arquivos de exemplo estão em: /examples/

1. exemplo1_basico.py - Criar objetos
2. exemplo2_scripts.py - Scripts com update()
3. exemplo3_input.py - Teclado e mouse
4. exemplo4_camera.py - Câmera e renderização
5. exemplo5_jogo_pong.py - Jogo completo

Rode qualquer um em um terminal ou estude o código!


═══════════════════════════════════════════════════════════

Divirta-se criando jogos! 🎮

Made with ❤️ for game developers
═══════════════════════════════════════════════════════════
""")
