import typer
from typing import Optional
from pathlib import Path
from ansible_workspace.models import AnsibleRole
from ansible_workspace.output import console
from ansible_workspace.misc import (
    find_ansible_roles_path,
    get_roles_config,
    handle_roles,
    add_roles_to_gitignore,
)
from ansible_workspace.tmuxp import TmuxpWorkspace, TmuxpWindow
from ansible_workspace.vscode import (
    VSCodeFolder,
    VSCodeWorkspace,
)
import importlib.metadata
import json
import yaml
from dataclasses import asdict

app = typer.Typer()


def general(
    roles_config: Optional[Path],
    ansible_config: Path,
    ansible_roles_path: Path,
    symlink_path: Optional[Path],
) -> list[AnsibleRole]:
    roles_path = ansible_roles_path or find_ansible_roles_path(ansible_config)

    roles = get_roles_config(roles_config)
    handle_roles(roles, roles_path, symlink_path)

    if str(Path().cwd()) in str(roles_path) and Path().cwd().joinpath(".git").exists():
        add_roles_to_gitignore(roles, roles_path)

    if (
        symlink_path
        and str(Path().cwd()) in str(symlink_path)
        and Path().cwd().joinpath(".git").exists()
    ):
        add_roles_to_gitignore(roles, symlink_path)
    return roles


@app.command()
def tmuxp(
    roles_config: Optional[Path] = typer.Option(
        None, "--roles-config", "-r", help="Path to roles config file"
    ),
    ansible_config: Path = typer.Option(
        Path.cwd().joinpath("ansible.cfg"), help="Path to ansible.cfg file"
    ),
    roles_path: Optional[Path] = typer.Option(
        None, envvar="ANSIBLE_ROLES_PATH", help="Path to the roles directory"
    ),
    symlink_path: Optional[Path] = typer.Option(
        None, help="Path to symlink the roles to"
    ),
    workspaces_path: Path = typer.Option(
        Path.home().joinpath("workspaces"),
        help="Path to the workspace directory",
        envvar='WORKSPACES_PATH',
    ),
):
    ansible_roles_path = roles_path or find_ansible_roles_path(ansible_config)
    roles = general(roles_config, ansible_config, ansible_roles_path, symlink_path)
    windows = []
    for role in roles:
        windows.append(
            TmuxpWindow(
                window_name=role.name,
                start_directory=str(ansible_roles_path.joinpath(role.name)),
            )
        )

    project_name = Path.cwd().name
    workspace = TmuxpWorkspace(
        session_name=project_name,
        start_directory=str(Path.cwd()),
        windows=[
            TmuxpWindow(
                window_name=project_name,
                start_directory=str(Path.cwd()),
            ),
            TmuxpWindow(
                window_name="ansible",
                start_directory=str(roles_path),
            ),
        ]
        + windows,
    )
    if not workspaces_path.exists():
        workspaces_path.mkdir(parents=True)
    config_path = workspaces_path.joinpath(f"{project_name}.tmuxp-workspace.yml")
    with open(config_path, "w") as f:
        yaml.safe_dump(asdict(workspace), f)
    console.print(f"Created workspace config at \"{config_path}\"")


@app.command()
def vscode(
    roles_config: Optional[Path] = typer.Option(
        None, "--roles-config", "-r", help="Path to roles config file"
    ),
    ansible_config: Path = typer.Option(
        Path.cwd().joinpath("ansible.cfg"), help="Path to ansible.cfg file"
    ),
    roles_path: Optional[Path] = typer.Option(
        None, envvar="ANSIBLE_ROLES_PATH", help="Path to the roles directory"
    ),
    symlink_path: Optional[Path] = typer.Option(
        None, help="Path to symlink the roles to"
    ),
    workspaces_path: Path = typer.Option(
        Path.home().joinpath("workspaces"),
        help="Path to the workspace directory",
        envvar='WORKSPACES_PATH',
    ),
):
    ansible_roles_path = roles_path or find_ansible_roles_path(ansible_config)
    roles = general(roles_config, ansible_config, ansible_roles_path, symlink_path)
    windows = []
    for role in roles:
        windows.append(
            VSCodeFolder(
                name=role.name,
                path=str(ansible_roles_path.joinpath(role.name)),
            )
        )

    project_name = Path.cwd().name
    workspace = VSCodeWorkspace(
        folders=[
            VSCodeFolder(
                name=project_name,
                path=str(Path.cwd()),
            ),
        ]
        + windows,
    )
    if not workspaces_path.exists():
        workspaces_path.mkdir(parents=True)
    config_path = workspaces_path.joinpath(f"{project_name}.code-workspace")
    with open(config_path, "w") as f:
        json.dump(asdict(workspace), f)
    console.print(f"Created workspace config at \"{config_path}\"")


@app.command()
def version():
    console.print(importlib.metadata.version('ansible-workspace'))
