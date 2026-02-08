"""Fortini Engine - Setup Script."""

from setuptools import setup, find_packages
from pathlib import Path

readme = Path(__file__).parent / "README.md"

setup(
    name="fortini-engine",
    version="1.0.0",
    description="A lightweight Python game engine with integrated editor",
    long_description=readme.read_text() if readme.exists() else "",
    long_description_content_type="text/markdown",
    author="Fortini Contributors",
    author_email="",
    url="https://github.com/Samuel45117/Fortini-Engine",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.5.0",
        "PyOpenGL>=3.1.5",
        "numpy>=1.24.0",
        "pygame>=2.1.0",
        "PyGLM>=2.5.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "pytest>=7.0.0",
            "isort>=5.0.0",
        ],
        "build": [
            "PyInstaller>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fortini-editor=fortini_engine.editor.run_editor:main",
            "fortini-engine=fortini_engine.core.engine:GameEngine",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
