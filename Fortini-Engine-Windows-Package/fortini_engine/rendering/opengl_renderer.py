"""OpenGL Rendering Engine."""

from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
from pathlib import Path
from fortini_engine.utils.logger import Logger


class Shader:
    """OpenGL Shader Program."""

    def __init__(self, vertex_src: str, fragment_src: str):
        self.program = None
        self._compile(vertex_src, fragment_src)

    def _compile(self, vertex_src: str, fragment_src: str) -> None:
        """Compile vertex and fragment shaders."""
        try:
            self.program = shaders.compileProgram(
                shaders.compileShader(vertex_src, GL_VERTEX_SHADER),
                shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER),
            )
        except Exception as e:
            logger = Logger().get_logger(self.__class__.__name__)
            logger.error(f"Shader compilation failed: {e}")
            self.program = None

    def use(self) -> None:
        """Use this shader program."""
        if self.program:
            glUseProgram(self.program)

    def set_mat4(self, name: str, mat: np.ndarray) -> None:
        """Set a 4x4 matrix uniform."""
        loc = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat)

    def set_vec3(self, name: str, x: float, y: float, z: float) -> None:
        """Set a 3D vector uniform."""
        loc = glGetUniformLocation(self.program, name)
        glUniform3f(loc, x, y, z)

    def set_float(self, name: str, value: float) -> None:
        """Set a float uniform."""
        loc = glGetUniformLocation(self.program, name)
        glUniform1f(loc, value)

    def set_int(self, name: str, value: int) -> None:
        """Set an int uniform."""
        loc = glGetUniformLocation(self.program, name)
        glUniform1i(loc, value)


class OpenGLRenderer:
    """OpenGL rendering engine."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.logger = Logger().get_logger(self.__class__.__name__)

        # Initialize OpenGL
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)

        # Create default shader
        self.default_shader = self._create_default_shader()

    def _create_default_shader(self) -> Shader:
        """Create default lighting shader."""
        vertex_shader = """
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
        """

        fragment_shader = """
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
            float ambientStrength = 0.1;
            vec3 ambient = ambientStrength * lightColor;

            // Diffuse
            vec3 norm = normalize(Normal);
            vec3 lightDir = normalize(lightPos - FragPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = diff * lightColor;

            // Specular
            float specularStrength = 0.5;
            vec3 viewDir = normalize(viewPos - FragPos);
            vec3 reflectDir = reflect(-lightDir, norm);
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
            vec3 specular = specularStrength * spec * lightColor;

            vec3 result = (ambient + diffuse + specular) * objectColor;
            FragColor = vec4(result, 1.0);
        }
        """

        return Shader(vertex_shader, fragment_shader)

    def render(self, scene, camera) -> None:
        """Render a scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, self.width, self.height)

        if not self.default_shader.program:
            return

        self.default_shader.use()

        # Get matrices
        view_matrix = camera.get_view_matrix().to_numpy()
        proj_matrix = camera.get_projection_matrix().to_numpy()

        # Set uniforms
        self.default_shader.set_mat4("view", view_matrix)
        self.default_shader.set_mat4("projection", proj_matrix)
        self.default_shader.set_vec3("viewPos", camera.transform.position.x, camera.transform.position.y, camera.transform.position.z)
        self.default_shader.set_vec3("lightColor", 1.0, 1.0, 1.0)
        self.default_shader.set_vec3("lightPos", 5.0, 5.0, 5.0)

        # Render objects
        for obj in scene.get_all_objects():
            if obj == camera or not obj.active:
                continue

            if obj.mesh is None:
                continue

            model_matrix = obj.transform.get_matrix().to_numpy()
            self.default_shader.set_mat4("model", model_matrix)

            # Set object color
            if obj.material:
                self.default_shader.set_vec3("objectColor", *obj.material.color[:3])
            else:
                self.default_shader.set_vec3("objectColor", 1.0, 1.0, 1.0)

            self._render_mesh(obj.mesh)

    def _render_mesh(self, mesh) -> None:
        """Render a mesh."""
        if mesh.vao is None:
            self._setup_mesh_buffers(mesh)

        if mesh.vao:
            glBindVertexArray(mesh.vao)
            glDrawElements(GL_TRIANGLES, len(mesh.indices), GL_UNSIGNED_INT, None)
            glBindVertexArray(0)

    def _setup_mesh_buffers(self, mesh) -> None:
        """Setup OpenGL buffers for a mesh."""
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        # Vertices
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, mesh.vertices.nbytes, mesh.vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Normals
        if len(mesh.normals) > 0:
            nbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, nbo)
            glBufferData(GL_ARRAY_BUFFER, mesh.normals.nbytes, mesh.normals, GL_STATIC_DRAW)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
            glEnableVertexAttribArray(1)

        # Indices
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, mesh.indices.nbytes, mesh.indices, GL_STATIC_DRAW)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        mesh.vao = vao
        mesh.vbo = vbo
        mesh.ebo = ebo

    def cleanup(self) -> None:
        """Clean up OpenGL resources."""
        self.logger.info("Cleaning up OpenGL resources")
        if self.default_shader.program:
            glDeleteProgram(self.default_shader.program)


import ctypes
