"""Project management system."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from fortini_engine.utils.logger import Logger


class Project:
    """Game project representation."""

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.logger = Logger().get_logger(self.__class__.__name__)

        # Project structure
        self.scenes_dir = path / "scenes"
        self.assets_dir = path / "assets"
        self.scripts_dir = path / "scripts"
        self.settings_dir = path / "settings"

        self._create_structure()

    def _create_structure(self) -> None:
        """Create project directory structure."""
        self.scenes_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        self.settings_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Project structure created at {self.path}")

    def save(self) -> None:
        """Save project metadata."""
        project_file = self.path / "project.json"
        data = {
            "name": self.name,
            "version": "1.0.0",
            "description": "A Fortini Engine project",
        }
        with open(project_file, "w") as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"Project saved: {project_file}")

    @staticmethod
    def load(path: Path) -> Optional["Project"]:
        """Load project from path."""
        project_file = path / "project.json"
        if not project_file.exists():
            return None

        with open(project_file, "r") as f:
            data = json.load(f)

        project = Project(data.get("name", "Unknown"), path)
        return project

    def __repr__(self) -> str:
        return f"Project(name='{self.name}', path={self.path})"


class ProjectManager:
    """Manage game projects."""

    def __init__(self):
        self.logger = Logger().get_logger(self.__class__.__name__)
        self.projects_dir = Path.home() / "Fortini Documents" / "Projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.current_project: Optional[Project] = None

    def create_project(self, name: str) -> Project:
        """Create a new project."""
        project_path = self.projects_dir / name
        if project_path.exists():
            self.logger.warning(f"Project already exists: {name}")
            return Project.load(project_path)

        project = Project(name, project_path)
        project.save()
        self.logger.info(f"Created project: {name}")
        return project

    def open_project(self, name: str) -> Optional[Project]:
        """Open an existing project."""
        project_path = self.projects_dir / name
        project = Project.load(project_path)
        if project:
            self.current_project = project
            self.logger.info(f"Opened project: {name}")
        return project

    def list_projects(self) -> list:
        """List all available projects."""
        projects = []
        for item in self.projects_dir.iterdir():
            if item.is_dir():
                project = Project.load(item)
                if project:
                    projects.append(project)
        return projects

    def delete_project(self, name: str) -> bool:
        """Delete a project."""
        project_path = self.projects_dir / name
        if not project_path.exists():
            self.logger.error(f"Project not found: {name}")
            return False

        import shutil

        shutil.rmtree(project_path)
        self.logger.info(f"Deleted project: {name}")
        return True
