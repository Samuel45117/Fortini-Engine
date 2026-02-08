"""
EXEMPLO 4: Câmera, Renderização e Iluminação

A engine suporta câmeras perspectiva e ortográfica.
A renderização usa OpenGL com iluminação Phong.
"""

from fortini_engine.core.camera import PerspectiveCamera, OrthographicCamera
from fortini_engine.core.game_object import GameObject
from fortini_engine.assets.manager import Material


def exemplo_camera():
    """Demonstrar sistemas de câmera."""
    
    print("📷 SISTEMA DE CÂMERA\n")
    
    # ============================================================
    # CÂMERA PERSPECTIVA (3D realista)
    # ============================================================
    
    print("📺 1. CÂMERA PERSPECTIVA (para 3D)")
    print("-" * 40)
    
    camera_3d = PerspectiveCamera(
        name="MainCamera",
        fov=45.0,          # Field of View (graus)
        aspect=16/9        # Proporção 16:9
    )
    
    print(f"✅ Câmera criada: {camera_3d.name}")
    print(f"   FOV: {camera_3d.fov}°")
    print(f"   Aspect: {camera_3d.aspect:.2f}")
    print(f"   Near plane: {camera_3d.near_plane}")
    print(f"   Far plane: {camera_3d.far_plane}")
    
    # Posicionar câmera
    camera_3d.transform.set_position(0, 2, 5)
    print(f"\n   Posição: {camera_3d.transform.position}")
    
    # Apontar para algo
    target = type('Vec3', (), {'x': 0, 'y': 0, 'z': 0})()
    print(f"   Olhando para: ({target.x}, {target.y}, {target.z})")
    
    # ============================================================
    # CÂMERA ORTOGRÁFICA (2D ou isométrica)
    # ============================================================
    
    print("\n\n📺 2. CÂMERA ORTOGRÁFICA (para 2D/UI)")
    print("-" * 40)
    
    camera_2d = OrthographicCamera(
        name="UICamera",
        left=-640,      # Bordas da visão
        right=640,
        bottom=-360,
        top=360
    )
    
    print(f"✅ Câmera criada: {camera_2d.name}")
    print(f"   Tamanho: {camera_2d.right - camera_2d.left} x {camera_2d.top - camera_2d.bottom}")
    print(f"   Near plane: {camera_2d.near_plane}")
    print(f"   Far plane: {camera_2d.far_plane}")


def exemplo_materiais():
    """Demonstrar sistema de materiais e iluminação."""
    
    print("\n\n🎨 SISTEMA DE MATERIAIS E CORES\n")
    
    # ============================================================
    # CRIAR MATERIAIS CUSTOMIZADOS
    # ============================================================
    
    print("Criando materiais customizados:")
    print("-" * 40)
    
    # Material vermelho
    mat_vermelho = Material("Vermelho")
    mat_vermelho.color = [1.0, 0.0, 0.0, 1.0]  # RGB + Alpha
    mat_vermelho.ambient = [0.2, 0.0, 0.0]
    mat_vermelho.diffuse = [0.8, 0.0, 0.0]
    mat_vermelho.shininess = 32.0
    
    print(f"✅ Material: {mat_vermelho.name}")
    print(f"   Cor: RGB{tuple(mat_vermelho.color[:3])}")
    print(f"   Shininess (brilho): {mat_vermelho.shininess}")
    
    # Material azul metálico
    mat_azul = Material("AzulMetalico")
    mat_azul.color = [0.0, 0.5, 1.0, 1.0]
    mat_azul.ambient = [0.3, 0.3, 0.5]
    mat_azul.diffuse = [0.4, 0.7, 1.0]
    mat_azul.specular = [1.0, 1.0, 1.0]
    mat_azul.shininess = 128.0  # Muito brilhante!
    
    print(f"\n✅ Material: {mat_azul.name}")
    print(f"   Cor: RGB{tuple(mat_azul.color[:3])}")
    print(f"   Shininess: {mat_azul.shininess}")
    
    # ============================================================
    # ILUMINAÇÃO PHONG
    # ============================================================
    
    print("\n\n💡 ILUMINAÇÃO (PHONG MODEL)")
    print("-" * 40)
    
    print("""
A engine usa iluminação Phong com 3 componentes:

1️⃣  AMBIENT (Luz ambiente)
   - Iluminação global, sem direção
   - Evita que o lado escuro fique completamente preto
   - Exemplo: mat_vermelho.ambient = [0.2, 0.0, 0.0]

2️⃣  DIFFUSE (Luz difusa)
   - Luz que vem de uma direção (ex: sol)
   - Mais brilhante quando virado para a luz
   - Exemplo: mat_vermelho.diffuse = [0.8, 0.0, 0.0]

3️⃣  SPECULAR (Reflexo especular)
   - Brilho/reflexo na superfície
   - Maior shininess = mais brilhante
   - Exemplo: mat_azul.specular = [1.0, 1.0, 1.0]
   
A luz é posicionada em: lightPos = [5, 5, 5]
E a câmera observa de: camera.position
    """)


def exemplo_renderizacao():
    """Mostrar pipeline de renderização."""
    
    print("🎬 PIPELINE DE RENDERIZAÇÃO\n")
    
    print("""
1️⃣  SETUP
    ├─ GameEngine.initialize()
    └─ OpenGLRenderer criado

2️⃣  CADA FRAME
    ├─ glClear() - Limpar tela
    ├─ Para cada objeto:
    │  ├─ Calcular Model Matrix (transf)
    │  ├─ Passar para shader
    │  └─ glDrawElements() - Renderizar mesh
    └─ Atualizar display

3️⃣  SHADERS (GLSL)
    ├─ VERTEX SHADER
    │  ├─ Transformar vértices (modelo → mundo → câmera)
    │  └─ Calcular normais
    │
    └─ FRAGMENT SHADER
       ├─ Calcular cor final
       ├─ Aplicar iluminação Phong
       └─ Retornar rgba

4️⃣  RESULTADO
    └─ Imagem 3D renderizada!
    """)


# ============================================================================
# EXEMPLO: USANDO CÂMERA E MATERIAIS
# ============================================================================

def exemplo_codigo():
    """Código exemplo."""
    
    codigo = '''# Seu código em um script:

from fortini_engine.core.camera import PerspectiveCamera
from fortini_engine.assets.manager import Material, AssetManager

class MeuJogo(Script):
    def start(self) -> None:
        # Configurar câmera
        camera = self.api.game_object.parent.parent  # Exemplo
        camera.transform.set_position(0, 5, 10)
        
        # Criar material customizado
        mat = Material("MeuMaterial")
        mat.color = [0.2, 0.8, 0.2, 1.0]  # Verde
        mat.shininess = 64.0
        
        # Aplicar objeto
        obj = GameObject("Cubo")
        obj.mesh = AssetManager().get_mesh("cube")
        obj.material = mat
    
    def update(self, delta_time: float) -> None:
        # Renderização acontece automaticamente!
        # Você só precisa atualizar posições e rotações
        pass
'''
    
    return codigo


if __name__ == "__main__":
    print("\n" + "="*50)
    print("   EXEMPLO 4: CÂMERA E RENDERIZAÇÃO")
    print("="*50 + "\n")
    
    exemplo_camera()
    exemplo_materiais()
    exemplo_renderizacao()
    
    print("\n" + "="*50)
    print("   CÓDIGO EXEMPLO")
    print("="*50)
    print(exemplo_codigo())
