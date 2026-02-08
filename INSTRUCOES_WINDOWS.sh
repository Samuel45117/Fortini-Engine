#!/bin/bash
# Script para exibir instruções de como usar o EXE no Windows

cat << 'INSTRUCOES'

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║        🎮 FORTINI ENGINE - COMO CRIAR EXE PARA WINDOWS                   ║
║                                                                            ║
║        Um executável pronto para distribuição no Windows                  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


📦 ARQUIVO GERADO:
   └─ Fortini-Engine-Windows-20260208.zip (96 KB)


═══════════════════════════════════════════════════════════════════════════════

🚀 PRÓXIMOS PASSOS:

1️⃣  TRANSFERIR PARA WINDOWS
   ──────────────────────────
   Opção A: Via Email/Cloud
   • Envie o ZIP para seu Windows
   • Google Drive, OneDrive, etc.
   
   Opção B: Via USB
   • Copie o ZIP para pendrive
   • Leve para Windows
   
   Opção C: Clonar Repositório
   • No Windows: git clone ...
   • Você já terá todos os arquivos


2️⃣  DESCOMPACTAR NO WINDOWS
   ────────────────────────
   • Clique com botão direito no ZIP
   • "Extract All..." ou "Extrair Aqui"
   
   Resultado:
   └─ Fortini-Engine-Windows-Package/
      ├─ fortini_engine/       (código da engine)
      ├─ launcher.py           (inicializador)
      ├─ build_exe_windows.bat (EXECUTAR ISTO!)
      ├─ requirements.txt      (dependências)
      └─ ... (outros arquivos)


3️⃣  COMPILAR PARA EXE (A PARTE IMPORTANTE!)
   ────────────────────────────────────────
   
   A. Requisitos no Windows:
      ✓ Python 3.10+ (https://www.python.org/)
        
        ⚠️  IMPORTANTE: Durante instalação:
        ✓ Marque: "Add Python to PATH"
        ✓ Marque: "Use admin privileges"
        
      ✓ Verificar:
        • Abra PowerShell ou CMD
        • Digite: python --version
        • Deve mostrar: Python 3.10.x ou superior
   
   B. Compilar:
      • Abra PowerShell ou CMD
      • Navegue para a pasta descompactada:
        cd C:\Users\Seu_Usuário\Downloads\Fortini-Engine-Windows-Package
      
      • Execute o script de compilação:
        .\build_exe_windows.bat
        
      • Espere 3-5 minutos...
      
      • Pronto! Seu EXE está em:
        dist\Fortini Editor\fortini_editor.exe


4️⃣  SEU EXE ESTÁ PRONTO! ✅
   ──────────────────────
   
   Localização:
   dist\Fortini Editor\fortini_editor.exe
   
   Clique para executar!


═══════════════════════════════════════════════════════════════════════════════

💡 DICAS:

✅ DISTRIBUIR:
   • Copie a pasta "Fortini Editor" para qualquer lugar
   • Crie atalho no desktop
   • Compacte em ZIP para enviar para outras pessoas


✅ PROBLEMAS?
   • Leia: BUILD_EXE_README.md (dentro do ZIP)
   • Leia: LEIA_PRIMEIRO.txt (dentro do ZIP)
   • Verifique se Python está instalado: python --version
   • Verifique se Python está no PATH


✅ AUTOMAÇÃO:
   • O arquivo build_exe_windows.bat faz tudo automaticamente
   • Você não precisa mexer em nada
   • Apenas espere e veja a "mágica" acontecer


═══════════════════════════════════════════════════════════════════════════════

📊 O QUE VAI ACONTECER DURANTE A COMPILAÇÃO:

1. Instalar PyInstaller (se não tiver)
2. Analisar código Python
3. Copiar dependências (PyQt6, PyOpenGL, NumPy, etc)
4. Empacotar tudo em um EXE
5. Criar pasta dist/Fortini Editor/

Tempo: 3-5 minutos
Tamanho final: 300-400 MB (inclui tudo!)


═══════════════════════════════════════════════════════════════════════════════

🎮 PRONTO PARA USAR NO WINDOWS!

Seu editor estará 100% funcional:
  ✓ Interface gráfica (PyQt6)
  ✓ Rendering 3D (OpenGL)
  ✓ Sistema de scripting Python
  ✓ Editor visual completo
  ✓ Tudo em um EXE


═══════════════════════════════════════════════════════════════════════════════

RESUMO RÁPIDO:

Windows                         | Ação
───────────────────────────────────────────────────────
1. Descompactar ZIP            → Extrair a pasta
2. Abrir Powershell/CMD        → cd Fortini-Engine-Windows-Package
3. Executar script             → .\build_exe_windows.bat
4. Aguardar                    → 3-5 minutos
5. EXE pronto!                 → dist\Fortini Editor\fortini_editor.exe


═══════════════════════════════════════════════════════════════════════════════

FIM DAS INSTRUÇÕES! 🎉

Qualquer dúvida:
• Leia os arquivos .md dentro do ZIP
• Verifique erros na tela (se houver)
• Certifique-se que Python está instalado

Sucesso na compilação! 🚀

INSTRUCOES

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
