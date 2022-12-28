from pathlib import Path
import os
import yaml
from configparser import ConfigParser
from typing import Optional
from ansible_workspace.models import AnsibleRole
from ansible_workspace.git import GitRepo
from ansible_workspace.output import console


def find_ansible_roles_path(ansible_cfg: Path) -> Path:
    """Find the path to the ansible roles directory."""
    if os.getenv("ANSIBLE_ROLES_PATH"):
        return Path(str(os.getenv("ANSIBLE_ROLES_PATH")))

    if Path.cwd().joinpath("roles").exists():
        return Path.cwd().joinpath("roles")

    if ansible_cfg.exists():
        config = parse_ansible_cfg(ansible_cfg)
        if config.has_option("defaults", "roles_path"):
            return Path(config["defaults"]["roles_path"])

    return Path().home().joinpath(".ansible", "roles")


def get_roles_config(source: Optional[Path] = None) -> list[AnsibleRole]:
    """Find the roles config file."""
    if source:
        config_path = Path(source)
    else:
        for path in Path.cwd().rglob("requirements.y*ml"):
            if not 'collections' in str(path):
                config_path = Path(path)
                break
        else:
            raise ValueError("Could not find the roles config file")

    config = yaml.safe_load(config_path.read_text())
    if isinstance(config, dict) and config.get("roles"):
        config = config["roles"]

    roles = []
    for role in config:
        if (
            isinstance(role, dict)
            and role.get("name")
            and role.get("src")
            and role.get("scm") == "git"
        ):
            roles.append(AnsibleRole(**role))
    return roles


def handle_roles(
    roles: list[AnsibleRole], roles_path: Path, symlink_path: Optional[Path] = None
) -> None:
    for role in roles:
        repo = GitRepo(role.src, roles_path.joinpath(role.name))
        if not roles_path.exists():
            roles_path.mkdir(parents=True)
        if not roles_path.joinpath(role.name).joinpath('.git').exists():
            repo.clone()
        repo.fetch_all()

        if role.version:
            if role.version in repo.get_tags():
                repo.checkout(role.version)
            elif role.version in repo.get_local_branches():
                repo.checkout(f'checkout {role.version}')
            elif f'origin/{role.version}' in repo.get_remote_branches():
                repo.checkout_remote_branch(role.version)
        else:
            if 'master' in repo.get_local_branches():
                repo.checkout('master')
            elif 'main' in repo.get_local_branches():
                repo.checkout('main')

        if symlink_path:
            symlink_role = symlink_path.joinpath(role.name)
            if symlink_role.exists():
                symlink_role.unlink()
            console.print(f"Symlinking \"{role.name}\" to \"{symlink_role}\"")
            symlink_role.symlink_to(repo.path)


def parse_ansible_cfg(path: Path) -> ConfigParser:
    """Parse the ansible.cfg file."""
    if not path.exists():
        raise ValueError("Could not find the ansible.cfg file")

    config = ConfigParser()
    config.read(str(path))
    return config


def add_roles_to_gitignore(roles: list[AnsibleRole], roles_path: Path) -> None:
    """Add the roles to the .gitignore file."""
    gitignore = Path.cwd().joinpath(".gitignore")
    if not gitignore.exists():
        gitignore.touch()
    for role in roles:
        cwd = Path.cwd()
        role_path = roles_path.joinpath(role.name)
        if not role.name in gitignore.read_text():
            with open(gitignore, "a") as f:
                relative_path = role_path.relative_to(cwd)
                console.print(f"Adding \"{relative_path}\" to .gitignore")
                f.write(f"{relative_path}/\n")
