"""Fortini Engine - Quick Start Guide."""

# Quick Start Guide - Fortini Engine

## 1. Installation

### On Windows/Mac/Linux:
```bash
# Clone the repository
git clone https://github.com/Samuel45117/Fortini-Engine.git
cd Fortini-Engine

# Install dependencies
pip install -r requirements.txt

# Install the engine in development mode
pip install -e .

# Launch the editor
python -m fortini_engine.editor.run_editor
```

## 2. Your First Game

### Step 1: Create a Scene
- Open the editor (see above)
- You should see an empty scene with a default cube

### Step 2: Add Objects
- Right-click in the Hierarchy panel
- Select "Create Cube" or "Create Sphere"

### Step 3: Edit Properties
- Click on an object in the Hierarchy
- In the Inspector panel, modify:
  - Position (X, Y, Z)
  - Rotation (Pitch, Yaw, Roll)
  - Scale (X, Y, Z)

### Step 4: Write a Script
Create a file `my_script.py` in your project's `scripts/` folder:

```python
from fortini_engine.scripting.script import Script
import math

class MyScript(Script):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.speed = 3.0
        self.time = 0

    def update(self, delta_time: float) -> None:
        self.time += delta_time
        # Rotate the object
        x = self.speed * math.sin(self.time)
        self.api.transform_translate(x, 0, 0)
```

### Step 5: Run Your Game
- Click the Play ▶ button in the editor
- Watch your scene come alive!
- Click Stop ⏹ to return to editing

## 3. Project Structure

When you create a new project, this structure is created:

```
~/Fortini Documents/Projects/MyGame/
├── scenes/              # Your game scenes
│   └── MainScene.scene
├── assets/             # Models, textures, audio
├── scripts/            # Your Python scripts
├── settings/           # Project configuration
└── project.json        # Project metadata
```

## 4. Publishing Your Game

### Export as Executable:
1. In the editor menu: **File > Export**
2. Enter your game name
3. (Optional) Choose a custom icon
4. Click **Build**
5. Your game is in `build/` folder!

## 5. Keyboard Controls in Editor

- **W/A/S/D**: Move camera (in viewport)
- **Middle Mouse**: Orbit camera
- **Scroll Wheel**: Zoom
- **Right-click object**: Object menu

## 6. Common Tasks

### Moving an Object
```python
self.api.transform_set_position(1, 2, 3)
# or relative movement:
self.api.transform_translate(0.1, 0, 0)
```

### Scaling an Object
```python
self.api.transform_set_scale(2, 2, 2)  # Double size
```

### Checking Object Name
```python
name = self.api.get_name()
if name == "Enemy":
    # Do something
    pass
```

### Control Visibility
```python
self.api.set_active(False)  # Hide
self.api.set_active(True)   # Show
```

## 7. Architecture Overview

The engine consists of:

1. **Core Engine** (`fortini_engine.core`)
   - GameEngine: Main coordinator
   - GameObject: Scene entities
   - Transform: Position/Rotation/Scale
   - Scene: Manages objects
   - Camera: View management

2. **Rendering** (`fortini_engine.rendering`)
   - OpenGL-based 3D rendering
   - Shader system
   - Mesh and material rendering

3. **Assets** (`fortini_engine.assets`)
   - Mesh management
   - Material system
   - Built-in primitives (Cube, Sphere, Pyramid)

4. **Scripting** (`fortini_engine.scripting`)
   - Python script system
   - CleanAPI for game logic

5. **Editor** (`fortini_engine.editor`)
   - PyQt6-based UI
   - Scene hierarchy
   - Inspector panel
   - Viewport rendering

6. **Utils** (`fortini_engine.utils`)
   - Math utilities (Vector3, Matrix4, Quaternion)
   - Logging system

## 8. Best Practices

### DO:
- ✅ Keep scripts focused and single-purpose
- ✅ Use meaningful object names
- ✅ Comment your scripts
- ✅ Test frequently with Play button
- ✅ Organize assets in folders

### DON'T:
- ❌ Use heavy loops in update()
- ❌ Create thousands of objects
- ❌ Ignore the logs/console
- ❌ Forget to save your work

## 9. Troubleshooting

**Q: "No OpenGL context"**
A: Update your graphics drivers

**Q: "PyQt6 not found"**
A: Run `pip install PyQt6`

**Q: My script isn't running**
A: Check the Console panel for errors

**Q: Game is very slow**
A: Check FPS counter, reduce object count or script complexity

## 10. Next Steps

1. Read the full [README.md](../README.md)
2. Check out [examples/](../examples/) directory
3. Explore the API reference in README
4. Join the community!

---

Happy game developing! 🎮
