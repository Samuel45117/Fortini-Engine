"""Fortini Engine - Technical Architecture Document."""

# Fortini Engine - Technical Architecture

## Overview

Fortini Engine is a modular Python game engine designed for:
- **Ease of use**: Simple, intuitive API
- **Extensibility**: Clean architecture for adding features
- **Performance**: Optimized rendering and scripting
- **Education**: Learn game engine design

## System Architecture

```
┌─────────────────────────────────────────────────┐
│          Editor UI (PyQt6)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ Viewport │  │Hierarchy │  │ Inspector    │ │
│  │ (OpenGL) │  │ (Tree)   │  │ (Properties) │ │
│  └──────────┘  └──────────┘  └──────────────┘ │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│       Game Engine Core                          │
│  ┌──────────────────────────────────────────┐  │
│  │ GameEngine (Main Coordinator)            │  │
│  ├──────────────────────────────────────────┤  │
│  │ • Time Management                        │  │
│  │ • Input System                           │  │
│  │ • Scene Management                       │  │
│  │ • GameObject Hierarchy                   │  │
│  │ • Camera System                          │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────┬──────────────────┐
│         Rendering Engine (OpenGL)        │  Asset Manager   │
│  ┌─────────────────────────────────────┐ │ ┌──────────────┐ │
│  │ • Mesh Rendering                    │ │ │ Meshes       │ │
│  │ • Shader System                     │ │ │ Materials    │ │
│  │ • Lighting (Ambient/Directional)    │ │ │ Textures     │ │
│  │ • Camera Projection                 │ │ └──────────────┘ │
│  │ • VAO/VBO Management                │ │                  │
│  └─────────────────────────────────────┘ │                  │
└──────────────────────────────────────────┴──────────────────┘
                      ↓
┌──────────────────────────────────────────┬──────────────────┐
│       Scripting System (Python)          │  Project Mgmt    │
│  ┌─────────────────────────────────────┐ │ ┌──────────────┐ │
│  │ • Script Loading/Execution          │ │ │ Project Path │ │
│  │ • Scripting API                     │ │ │ Save/Load    │ │
│  │ • Transform API                     │ │ │ Export       │ │
│  │ • Object API                        │ │ └──────────────┘ │
│  └─────────────────────────────────────┘ │                  │
└──────────────────────────────────────────┴──────────────────┘
```

## Module Breakdown

### 1. Core Engine (`fortini_engine.core`)

#### GameEngine
```python
class GameEngine:
    - initialize(width, height, title)
    - update()              # Per-frame update
    - render()              # Per-frame render
    - run()                 # Main loop
    - shutdown()            # Cleanup
    - set_scene(scene)      # Switch scenes
```

#### GameObject
```python
class GameObject:
    - transform: Transform
    - components: Dict
    - children: List
    - add_child(child)
    - add_component(name, component)
    - update(delta_time)
    - to_dict() / from_dict()
```

#### Transform
```python
class Transform:
    - position: Vector3
    - rotation: Quaternion
    - scale: Vector3
    - parent: Transform
    - children: List[Transform]
    - translate(x, y, z)
    - set_position/rotation/scale()
    - get_matrix()          # Model matrix
```

#### Scene
```python
class Scene:
    - name: str
    - objects: List[GameObject]
    - root_objects: List[GameObject]
    - main_camera: Camera
    - add_object(obj, parent=None)
    - find_object(name)
    - update(delta_time)
    - get_hierarchy()
```

#### Camera System
```python
class Camera(GameObject):
    - get_view_matrix()
    - get_projection_matrix()
    - look_at(target)

class PerspectiveCamera(Camera):
    - fov: float
    - aspect: float
    - near_plane, far_plane

class OrthographicCamera(Camera):
    - left, right, bottom, top
```

#### Time & Input
```python
class Time:
    - delta_time: float
    - elapsed_time: float
    - fps: float
    - update()

class Input:
    - is_key_pressed(key)
    - is_mouse_button_pressed(button)
    - get_mouse_position()
    - register_key_callback(key, callback)
```

### 2. Rendering Engine (`fortini_engine.rendering`)

#### Shader Program
```python
class Shader:
    - program: GLuint
    - use()
    - set_mat4(name, mat)
    - set_vec3(name, x, y, z)
    - set_float(name, value)
    - set_int(name, value)
```

#### OpenGLRenderer
```python
class OpenGLRenderer:
    - width, height: int
    - default_shader: Shader
    - render(scene, camera)
    - _render_mesh(mesh)
    - _setup_mesh_buffers(mesh)
    - cleanup()
```

**Shader Pipeline:**
- Vertex shader: Transforms vertices and normals
- Fragment shader: Calculates lighting (Phong model)
- Uniforms: model, view, projection, light position, camera position

### 3. Assets (`fortini_engine.assets`)

#### Mesh
```python
class Mesh:
    - vertices: np.ndarray (Nx3)
    - normals: np.ndarray (Nx3)
    - uv_coords: np.ndarray (Nx2)
    - indices: np.ndarray (faces)
    - vao, vbo, ebo: GLuint
    
    - add_cube(size)
    - add_sphere(radius, sectors, stacks)
    - add_pyramid(size)
    - calculate_normals()
```

#### Material
```python
class Material:
    - color: [R, G, B, A]
    - ambient, diffuse, specular
    - shininess: float
    - texture: optional
    - shader: optional
```

#### AssetManager
```python
class AssetManager:
    - _meshes: Dict[str, Mesh]
    - _materials: Dict[str, Material]
    - _textures: Dict[str, GLuint]
    
    - register_mesh(name, mesh)
    - get_mesh(name)
    - create_default_assets()
```

### 4. Scripting (`fortini_engine.scripting`)

#### Script Base Class
```python
class Script:
    - game_object: GameObject
    - api: ScriptingAPI
    
    - start()               # Called on init
    - update(delta_time)    # Called per frame
    - on_destroy()          # Called on removal
```

#### ScriptingAPI
```python
class ScriptingAPI:
    - transform_translate(x, y, z)
    - transform_set_position(x, y, z)
    - transform_set_rotation(pitch, yaw, roll)
    - transform_set_scale(x, y, z)
    - get_position() -> tuple
    - get_scale() -> tuple
    - set_active(bool)
    - get_name() -> str
```

#### ScriptManager
```python
class ScriptManager:
    - load_script(path) -> type
    - create_script_instance(script_class, game_object)
    - load_and_attach_script(path, game_object)
```

### 5. Editor UI (`fortini_engine.editor`)

#### FortiniEditor (Main Window)
```
┌─────────────────────────────────────────┐
│ Menu Bar | Toolbar (Play/Stop/FPS)      │
├──────────┬──────────────┬───────────────┤
│          │              │               │
│Hierarchy │  3D Viewport │   Inspector   │
│ Panel    │  (OpenGL)    │    Panel      │
│(Tree)    │              │(Properties)   │
│          │              │               │
├──────────┴──────────────┴───────────────┤
│ Asset Browser                           │
├─────────────────────────────────────────┤
│ Console / Log Output                    │
└─────────────────────────────────────────┘
```

#### Panels

**ViewportPanel**: OpenGL widget for scene rendering
- Mouse controls: Middle button to orbit
- Scroll wheel to zoom
- Renders scene with active camera

**HierarchyPanel**: Tree view of scene objects
- Shows parent-child relationships
- Click to select objects
- Emits `object_selected` signal

**InspectorPanel**: Property editor
- Displays selected object properties
- Position, rotation, scale inputs
- Real-time updates

**AssetBrowserPanel**: Asset listing
- Shows available meshes
- Lists materials
- Texture browser (future)

**ConsolePanel**: Log output
- Engine messages
- Debug information
- Error reporting

### 6. Project Management (`fortini_engine.editor`)

#### Project
```python
class Project:
    - name: str
    - path: Path
    - scenes_dir, assets_dir, scripts_dir, settings_dir
    - save()
    - load(path) -> Project
```

#### ProjectManager
```python
class ProjectManager:
    - projects_dir: Path
    - current_project: Optional[Project]
    - create_project(name) -> Project
    - open_project(name) -> Project
    - list_projects() -> List[Project]
```

## Data Flow

### Initialization
```
Editor Start
    ↓
GameEngine.initialize()
    ├─ pygame.init()
    ├─ OpenGL setup
    ├─ Create default scene
    ├─ AssetManager.create_default_assets()
    └─ Create main camera
    ↓
UI Panels initialized
    ├─ Hierarchy from scene
    ├─ Inspector empty (no selection)
    └─ Viewport ready
```

### Main Game Loop (Editor Mode)
```
Timer Tick (16ms ≈ 60 FPS)
    ↓
Time.update() → calculate delta_time
    ↓
Input.update() → process pygame events
    ↓
Scene.update(delta_time)
    ├─ For each root object:
    │   └─ GameObject.update(delta_time)
    │       ├─ Script.update(delta_time)
    │       └─ Update children
    ↓
Renderer.render(scene, camera)
    ├─ glClear()
    ├─ For each object:
    │   ├─ Get model matrix
    │   └─ Render mesh with shader
    ↓
UI update (FPS label, etc.)
```

### Play Mode
```
Click Play
    ↓
Scene state saved
    ↓
Main loop continues with:
    - Scripts and objects updating
    - Physics (future)
    - Input handling
    ↓
Click Stop
    ↓
Restore original scene state
    ↓
Return to editing
```

### Export Process
```
File > Export
    ↓
User enters game name + icon
    ↓
Create standalone directory
    ├─ Copy project files
    ├─ Copy engine core
    └─ Package scripts
    ↓
PyInstaller build
    ├─ Bundle Python runtime
    ├─ Package all dependencies
    └─ Add icon/metadata
    ↓
Generate executable
```

## Rendering Pipeline

### Vertex Processing
```glsl
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 FragPos;
out vec3 Normal;

void main()
{
    FragPos = vec3(model * vec4(position, 1.0));
    Normal = mat3(transpose(inverse(model))) * normal;
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
```

### Fragment Processing (Phong Lighting)
```glsl
#version 330 core
in vec3 FragPos;
in vec3 Normal;

uniform vec3 objectColor;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;

out vec4 FragColor;

void main()
{
    // Ambient
    vec3 ambient = 0.1 * lightColor;
    
    // Diffuse
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    
    // Specular
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = 0.5 * spec * lightColor;
    
    vec3 result = (ambient + diffuse + specular) * objectColor;
    FragColor = vec4(result, 1.0);
}
```

## Memory Management

### Asset Lifecycle
```
AssetManager.create_default_assets()
    ├─ Cube mesh → GPU (VAO/VBO)
    ├─ Sphere mesh → GPU
    ├─ Pyramid mesh → GPU
    └─ Default material

GameObject references mesh → CPU
    ├─ Mesh contains GPU handles
    └─ Updated on first render

On Cleanup:
    glDeleteBuffers() → VAO, VBO, EBO
    glDeleteProgram() → Shaders
```

### Script Lifecycle
```
ScriptManager.load_script(path)
    ├─ importlib.util.spec_from_file_location()
    └─ module.exec_module()

Script instance created: Script(game_object)
    ├─ Script.start() called
    └─ Attached to game_object.script

Every frame: game_object.script.update(delta_time)

On destruction: Script.on_destroy()
```

## Extension Points

### Custom Shaders
```python
from fortini_engine.rendering.opengl_renderer import Shader

vertex_src = "..."
fragment_src = "..."
custom_shader = Shader(vertex_src, fragment_src)
```

### Custom Components
```python
class CustomComponent:
    def __init__(self, data):
        self.data = data
    
    def update(self, delta_time):
        pass

obj.add_component("custom", CustomComponent({"key": "value"}))
custom = obj.get_component("custom")
```

### Custom Meshes
```python
from fortini_engine.assets.manager import Mesh, AssetManager

custom_mesh = Mesh("CustomMesh")
custom_mesh.vertices = np.array([...])
custom_mesh.indices = np.array([...])
custom_mesh.calculate_normals()

AssetManager().register_mesh("custom", custom_mesh)
```

## Performance Considerations

1. **Rendering**
   - VAO/VBO cached on first use
   - Depth testing enabled
   - Culling ready (future)

2. **Scripting**
   - Scripts called in update loop
   - Use dt for framerate independence

3. **Scene Hierarchy**
   - Recursive update through hierarchy
   - Transform matrix caching with dirty flags

4. **Memory**
   - Python GC handles most cleanup
   - GPU resources cleaned on shutdown

## Future Extensions

- Physics engine (Bullet/Rapier)
- Audio system
- Particle effects
- Animation system
- Advanced materials (PBR)
- Network multiplayer
- Terrain system
- UI toolkit

---

**Architecture follows:** Component-Entity System, Hybrid Rendering Pipeline, Modular Plugin Architecture
