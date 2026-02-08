"""
EXEMPLO 1: Seu Primeiro Programa com Fortini

Este arquivo mostra como usar a engine de forma básica,
sem o editor - apenas código Python puro.
"""

from fortini_engine.core.engine import GameEngine
from fortini_engine.core.game_object import GameObject
from fortini_engine.core.camera import PerspectiveCamera
from fortini_engine.assets.manager import AssetManager


def main():
    # ✅ Passo 1: Criar engine
    engine = GameEngine()
    engine.initialize(width=800, height=600, title="Meu Primeiro Jogo")
    
    print(f"✅ Engine criado: {engine}")
    print(f"✅ Cena ativa: {engine.current_scene.name}")
    
    # ✅ Passo 2: Obter gerenciador de assets
    asset_manager = AssetManager()
    
    # ✅ Passo 3: Criar objetos na cena
    # Cubo 1
    cube1 = GameObject("Cubo1")
    cube1.mesh = asset_manager.get_mesh("cube")
    cube1.material = asset_manager.get_material("default")
    cube1.transform.set_position(0, 0, 0)
    cube1.transform.set_scale(1, 1, 1)
    engine.current_scene.add_object(cube1)
    
    print(f"✅ Objeto criado: {cube1}")
    print(f"   Posição: {cube1.transform.position}")
    print(f"   Escala: {cube1.transform.scale}")
    
    # Outro cubo
    cube2 = GameObject("Cubo2")
    cube2.mesh = asset_manager.get_mesh("sphere")
    cube2.material = asset_manager.get_material("default")
    cube2.transform.set_position(3, 0, 0)
    engine.current_scene.add_object(cube2)
    
    # ✅ Passo 4: Visualizar cena
    print(f"\n📊 Cena contém {len(engine.current_scene.objects)} objetos:")
    for obj in engine.current_scene.objects:
        print(f"   - {obj.name} em {obj.transform.position}")
    
    # ✅ Passo 5: Modificar objetos
    print(f"\n🔧 Modificando cubo 1...")
    cube1.transform.translate(1, 0, 0)  # mover
    print(f"   Nova posição: {cube1.transform.position}")
    
    # ✅ Passo 6: Procurar objetos
    print(f"\n🔍 Procurando objeto 'Cubo2'...")
    encontrado = engine.current_scene.find_object("Cubo2")
    if encontrado:
        print(f"   ✅ Encontrado: {encontrado.name}")
    
    # ✅ Passo 7: Desativar objeto
    print(f"\n👁️  Desativando Cubo2...")
    cube2.set_active(False)
    print(f"   Ativo? {cube2.active}")
    
    print("\n" + "="*50)
    print("✅ Exemplo 1 completo!")
    print("="*50)


if __name__ == "__main__":
    main()
