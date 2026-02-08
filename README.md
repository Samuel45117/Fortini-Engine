# Fortini Engine

A lightweight, modular Python game engine with an integrated editor, designed for indie and hobby developers.

## Features

### 🎮 Core Engine
- **OpenGL Rendering**: Modern 3D rendering with support for meshes, materials, and textures
- **3D Object System**: Hierarchical scene graph with transform inheritance
- **Camera System**: Perspective and orthographic cameras with editor controls
- **Physics-Ready**: Built for easy physics integration
- **Python Scripting**: Write game logic in pure Python with a clean API

### 🎨 Editor Interface
- **Visual Hierarchy Panel**: Drag-and-drop scene tree
- **Inspector Panel**: Edit object properties in real-time
- **3D Viewport**: Interactive scene preview with camera controls
- **Asset Browser**: Manage and organize game assets
- **Console Output**: View engine logs and debug messages

### 🛠️ Project Management
- **Project Structure**: Organized directory layout with scenes, assets, and scripts
- **Auto-Save**: Projects persist automatically
- **Multiple Projects**: Support for unlimited projects in `~/Fortini Documents/Projects/`

### 📦 Export System
- **Standalone Executables**: Export games as `.exe` or platform-specific binaries
- **PyInstaller Integration**: One-click build process
- **Custom Icons**: Add branding to your exports

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- OpenGL-compatible graphics card

### Quick Start

1. **Clone the repository:**
\`\`\`bash
git clone https://github.com/Samuel45117/Fortini-Engine.git
cd Fortini-Engine
\`\`\`

2. **Install dependencies:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Install Fortini locally:**
\`\`\`bash
pip install -e .
\`\`\`

4. **Launch the editor:**
\`\`\`bash
python -m fortini_engine.editor.run_editor
\`\`\`

## Architecture

### Directory Structure

\`\`\`
Fortini-Engine/
├── fortini_engine/
│   ├── core/               # Engine core (engine, scene, objects, camera)
│   ├── rendering/          # OpenGL rendering engine
│   ├── editor/             # Editor UI and panels
│   ├── scripting/          # Python scripting system
│   ├── assets/             # Asset management
│   ├── utils/              # Math, logging, utilities
│   └── __init__.py
├── examples/               # Example scripts and projects
├── setup.py               # Installation configuration
├── requirements.txt       # Dependencies
└── README.md              # This file
\`\`\`

### Core Modules

#### \`fortini_engine.core\`
- **\`engine.py\`**: Main \`GameEngine\` class - ties everything together
- **\`game_object.py\`**: \`GameObject\` class - base for all scene entities
- **\`transform.py\`**: \`Transform\` component - position, rotation, scale
- **\`scene.py\`**: \`Scene\` class - manages game objects and hierarchy
- **\`camera.py\`**: \`Camera\`, \`PerspectiveCamera\`, \`OrthographicCamera\`
- **\`time.py\`**: Time management (delta time, FPS)
- **\`input.py\`**: Input management (keyboard, mouse)

#### \`fortini_engine.rendering\`
- **\`opengl_renderer.py\`**: OpenGL rendering engine with shader support
- Handles mesh rendering, lighting, and camera setup

#### \`fortini_engine.assets\`
- **\`manager.py\`**: \`AssetManager\` for meshes, materials, and textures
- Built-in mesh generators (cube, sphere, pyramid)

#### \`fortini_engine.scripting\`
- **\`script.py\`**: \`Script\` base class and \`ScriptingAPI\`
- Allows users to write game logic in Python

#### \`fortini_engine.editor\`
- **\`main.py\`**: Main editor window
- **\`project_manager.py\`**: Project creation and management
- **\`panels/\`**: UI components (viewport, hierarchy, inspector, etc.)

## Usage

### Creating a Game

1. **Launch the editor:**
\`\`\`bash
python -m fortini_engine.editor.run_editor
\`\`\`

2. **Create objects:**
   - Right-click in the Hierarchy to add objects
   - Select from: Cube, Sphere, Pyramid, Empty Object

3. **Edit properties:**
   - Select objects in the Hierarchy
   - Modify position, rotation, scale in the Inspector

4. **Write scripts:**
   - Create a Python file in \`Scripts/\`
   - Attach to objects via the editor

5. **Run the game:**
   - Press the Play button in the editor
   - Press Stop to return to editing

### Writing Scripts

Scripts inherit from \`Script\` and have access to the \`ScriptingAPI\`:

\`\`\`python
from fortini_engine.scripting.script import Script


class MyScript(Script):
    """Custom script for my game object."""

    def __init__(self, game_object):
        super().__init__(game_object)
        self.speed = 5.0

    def start(self) -> None:
        """Called when the game starts."""
        print(f"Started script for {self.api.get_name()}")

    def update(self, delta_time: float) -> None:
        """Called every frame."""
        # Move the object
        self.api.transform_translate(
            self.speed * delta_time, 0, 0
        )

    def on_destroy(self) -> None:
        """Called when the object is destroyed."""
        print("Script ended")
\`\`\`

### API Reference

#### Transform API
\`\`\`python
api.transform_translate(x, y, z)        # Move relative
api.transform_set_position(x, y, z)     # Set absolute position
api.transform_set_rotation(pitch, yaw, roll)  # Set rotation (radians)
api.transform_set_scale(x, y, z)        # Set scale
api.get_position()                       # Returns (x, y, z)
api.get_scale()                          # Returns (x, y, z)
\`\`\`

#### Object API
\`\`\`python
api.set_active(True/False)               # Show/hide object
api.get_name()                           # Get object name
\`\`\`

## Scripting Examples

See the \`examples/\` directory for sample scripts:
- \`simple_movement.py\`: Basic object movement
- \`rotating_cube.py\`: Rotation implementation
- \`camera_controller.py\`: Camera control

## Project Structure (User Projects)

When you create a project, this structure is generated:

\`\`\`
~/Fortini Documents/Projects/MyGame/
├── scenes/               # Scene files (.scene)
├── assets/              # 3D models, textures, etc.
├── scripts/             # Python game scripts
├── settings/            # Project configuration
└── project.json         # Project metadata
\`\`\`

## Exporting Games

To export your game as a standalone executable:

1. In the editor, click **File > Export**
2. Choose a game name
3. (Optional) Select a custom icon
4. Click **Build**
5. The executable will be created in \`build/\`

Exports use PyInstaller to bundle Python and all dependencies.

## Graphics Pipeline

### Rendering Features
- ✅ 3D mesh rendering
- ✅ Basic lighting (ambient + directional)
- ✅ Material system
- ✅ Depth testing and culling
- ✅ Viewport management
- 🔜 Texturing support
- 🔜 Normal mapping
- 🔜 Skybox system

### Shader System
- Vertex and fragment shader support
- Built-in lighting shader
- Custom shader creation ready

## Input System

### Keyboard Input
\`\`\`python
from fortini_engine.core.input import Input

input_manager = Input()
if input_manager.is_key_w_pressed():
    # Handle W key
    pass

# Common shortcuts
input_manager.is_key_a_pressed()      # A
input_manager.is_key_s_pressed()      # S
input_manager.is_key_d_pressed()      # D
input_manager.is_key_space_pressed()  # Space
input_manager.is_key_escape_pressed() # Escape
\`\`\`

### Mouse Input
\`\`\`python
input_manager.get_mouse_position()     # Returns (x, y)
input_manager.is_mouse_button_pressed(1)  # Left click
\`\`\`

## Performance

- **Target**: 60 FPS on modern hardware
- **Optimization**: Frustum culling, depth testing, VAO/VBO caching
- **Memory**: Minimal footprint (~50MB base)

## Scene System

### Hierarchy & Transform Inheritance

Objects have parent-child relationships:

\`\`\`python
parent_obj = GameObject("Parent")
child_obj = GameObject("Child")

parent_obj.add_child(child_obj)

# Child inherits parent's transform
parent_obj.transform.translate(1, 0, 0)  # Child moves too!
\`\`\`

### Active State

Control object visibility and updates:

\`\`\`python
obj.set_active(False)  # Hide and disable updates
obj.set_active(True)   # Show and enable updates
\`\`\`

## Debugging

The engine logs all activities to:
- Console (stdout)
- Log file: \`~/Fortini Documents/Logs/fortini_*.log\`

Check these for troubleshooting.

## Contributing

Contributions are welcome! Areas for expansion:
- Physics engine integration (Bullet, Rapier)
- Animation system
- Particle effects
- Audio system
- Advanced lighting (PBR)
- Terrain system
- UI toolkit
- Networking

## Roadmap

### v1.0 (Current)
- ✅ Basic rendering engine
- ✅ Scene management
- ✅ Python scripting
- ✅ Editor UI
- ✅ Project management

### v1.1 (Planned)
- 🔜 Skybox system
- 🔜 Texture support
- 🔜 Simple physics (colliders)
- 🔜 Audio system

### v2.0 (Future)
- 🔜 Advanced materials & PBR
- 🔜 Particle effects
- 🔜 Animation system
- 🔜 Networking support

## Troubleshooting

### OpenGL Not Initialized
**Problem**: "OpenGL context not initialized"
**Solution**: Ensure you have a compatible graphics card and drivers installed.

### PyQt6 Issues
**Problem**: "No module named 'PyQt6'"
**Solution**: Run \`pip install PyQt6\`

### Pygame Initialization Failed
**Problem**: "Pygame initialization error"
**Solution**: The editor needs Pygame. Run \`pip install -r requirements.txt\`

## Performance Tips

1. **Use LOD (Level of Detail)**: Create simpler meshes for distant objects
2. **Batch Rendering**: Group similar objects for better performance
3. **Optimize Scripts**: Avoid heavy computations in \`update()\`
4. **Profile**: Use the FPS counter to identify bottlenecks

## License

MIT License

## Citation

If you use Fortini Engine in your project, please cite:
\`\`\`bibtex
@software{fortini_engine,
  title = {Fortini Engine},
  author = {Samuel45117 and contributors},
  year = {2024},
  url = {https://github.com/Samuel45117/Fortini-Engine}
}
\`\`\`

## Support

- 📖 Documentation: See this README
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

## Credits

**Inspired by**: Unity, Godot, Unreal Engine  
**Built with**: PyOpenGL, PyQt6, NumPy, Pygame  
**For**: Indie & hobby game developers

---

**Made with ❤️ for game developers everywhere**
