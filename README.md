# ansible-workspace

Create a workspace for multiple tools to easier develop ansible playbooks with roles.

Roles with a reference to a git repository will be cloned, checked out and added to the workspace.

The `.gitignore` will be configured to ignore the role repositories or symlinks.

## Install

```bash
pip install -U ansible-workspace
```

or with [pipx](https://github.com/pypa/pipx)

```bash
pipx install ansible-workspace
```

## Workspaces

```bash
ansible-workspace --help
```

### General

#### Symlinks

If you want your roles in e.g. `~/ansible-roles` but want to symlink them to `./roles` use the following command:

```bash
ansible-workspace <tool> --roles-path ~/ansible-roles --symlink-path roles/
```

### [VSCode](https://code.visualstudio.com/)

The workspace consists of:
- A folder for the playbook directory
- A folder for each role defined in the requirements

```bash
ansible-workspace vscode
```

```bash
code ~/workspaces/example-project.code-workspace
```

### [tmuxp](https://github.com/tmux-python/tmuxp)

The workspace consists of:
- A window for the playbook directory
- A window to exectute ansible commands
- A window for each role defined in the requirements

```bash

```bash
ansible-workspace tmuxp
```

```bash
tmuxp load -y ~/workspaces/example-project.tmuxp-workspace.yml
```

## Examples

The following roles are defined under `roles/requirements.yml`:

```yaml
---
roles:
  - name: role1
    version: v1.0.3
    src: git@github.com:rwxd/ansible-role-subuid_subgid.git
    scm: git

  - name: role2
    version: v1.0.2
    src: git@github.com:rwxd/ansible-role-subuid_subgid.git
    scm: git

  - name: role3
    version: master
    src: git@github.com:rwxd/ansible-role-subuid_subgid.git
    scm: git
```

```bash
❯ ansible-workspace vscode
Cloning "git@github.com:rwxd/ansible-role-subuid_subgid.git" to "/tmp/test_repo/roles/role1"
Checking out "v1.0.3" on "git@github.com:rwxd/ansible-role-subuid_subgid.git"
Cloning "git@github.com:rwxd/ansible-role-subuid_subgid.git" to "/tmp/test_repo/roles/role2"
Checking out "v1.0.2" on "git@github.com:rwxd/ansible-role-subuid_subgid.git"
Cloning "git@github.com:rwxd/ansible-role-subuid_subgid.git" to "/tmp/test_repo/roles/role3"
Adding "roles/role1" to .gitignore
Adding "roles/role2" to .gitignore
Adding "roles/role3" to .gitignore
Created workspace config at "/home/<name>/workspaces/test_repo.code-workspace"
```

The workspace can now be opened with `code ~/workspaces/test_repo.code-workspace`.
