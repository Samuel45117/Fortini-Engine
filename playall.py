#!/usr/bin/env python3
"""
playall.py — comando único para iniciar a Fortini Engine

Uso:
  py playall.py           # no Windows (py launcher)
  python3 playall.py      # no Linux/macOS

Opções:
  --mode MODE    : 'editor' (default) ou 'example1'..'example5'
  --no-gui       : testar checagens sem abrir janela (útil em CI/headless)
  --install      : instalar dependências antes de rodar (pip install -r requirements.txt)

O script tentará importar e iniciar o editor via `launcher.py`.
"""

import sys
import argparse
import subprocess
import os


def install_requirements():
    req = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req):
        print('Instalando dependências (requirements.txt)...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req])
    else:
        print('requirements.txt não encontrado — pulando instalação')


def run_no_gui_checks():
    print('Executando checagens (no-gui)...')
    try:
        import PyQt6
        import OpenGL
        import numpy
        import pygame
        print('Dependências principais encontradas: PyQt6, PyOpenGL, numpy, pygame')
    except Exception as e:
        print('Aviso: dependência faltando ou erro ao importar:', e)
        print('Use `py playall.py --install` para instalar dependências')
    print('OK — modo no-gui terminado.')


def start_editor():
    # Preferir launcher.py (Ponto de entrada seguro)
    launcher = os.path.join(os.path.dirname(__file__), 'launcher.py')
    if os.path.exists(launcher):
        print('Iniciando editor via launcher.py...')
        # Exec the launcher in the current interpreter so PyQt runs in-process
        with open(launcher, 'rb') as f:
            code = compile(f.read(), launcher, 'exec')
            exec(code, {'__name__': '__main__'})
    else:
        # fallback: módulo entrypoint
        print('launcher.py não encontrado — tentando módulo `fortini_engine.editor.run_editor`')
        subprocess.check_call([sys.executable, '-m', 'fortini_engine.editor.run_editor'])


def start_example(name):
    # exemplos oferecidos: exemplo1_basico.py ... exemplo5_jogo_pong.py
    examples = {
        'example1': 'exemplo1_basico.py',
        'example2': 'exemplo2_scripts.py',
        'example3': 'exemplo3_input.py',
        'example4': 'exemplo4_camera.py',
        'example5': 'exemplo5_jogo_pong.py',
    }
    key = name.lower()
    if key in examples:
        path = os.path.join(os.path.dirname(__file__), examples[key])
        if os.path.exists(path):
            print(f'Iniciando exemplo: {path}')
            subprocess.check_call([sys.executable, path])
        else:
            print('Exemplo não encontrado:', path)
    else:
        print('Exemplo inválido. Opções:', ','.join(examples.keys()))


def main():
    parser = argparse.ArgumentParser(description='Playall — iniciar Fortini Editor/exemplos')
    parser.add_argument('--mode', default='editor', help="'editor' ou 'example1'..'example5'")
    parser.add_argument('--no-gui', action='store_true', help='rodar apenas checagens sem abrir janela')
    parser.add_argument('--install', action='store_true', help='instalar dependências antes de rodar')
    args = parser.parse_args()

    if args.install:
        install_requirements()

    if args.no_gui:
        run_no_gui_checks()
        return

    if args.mode == 'editor':
        start_editor()
    elif args.mode.startswith('example'):
        start_example(args.mode)
    else:
        print('Modo desconhecido:', args.mode)


if __name__ == '__main__':
    main()
