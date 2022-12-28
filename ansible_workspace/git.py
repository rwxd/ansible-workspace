from subprocess import check_output, STDOUT, CalledProcessError, Popen, PIPE
from ansible_workspace.output import console
from pathlib import Path


class GitRepo:
    def __init__(self, source: str, path: Path):
        self.source = source
        self.path: Path = path

    def run(self, *args) -> str:
        try:
            process = Popen(
                ('git', '-C', str(self.path), *args), stdout=PIPE, stderr=PIPE
            )
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise CalledProcessError(
                    process.returncode, process.args, output=stdout, stderr=stderr
                )
            return stdout.decode('utf-8')
        except CalledProcessError as e:
            console.print(e.output.decode('utf-8'))
            console.print(e.stderr.decode('utf-8'))
            raise ValueError(f"Failed to run git command: {e.cmd}") from e

    def checkout(self, branch: str) -> str:
        console.print(f"Checking out \"{branch}\" on \"{self.path}\"")
        return self.run('checkout', branch)

    def checkout_remote_branch(self, branch: str) -> str:
        console.print(
            f"Checking out \"{branch}\" from \"origin/{branch}\" on \"{self.source}\""
        )
        return self.run('checkout', '-b', branch, f'origin/{branch}')

    def clone(self) -> str:
        if not self.path.exists():
            self.path.mkdir(parents=True)
        console.print(f"Cloning \"{self.source}\" to \"{self.path}\"")
        return self.run('clone', self.source, '.')

    def fetch_all(self) -> str:
        return self.run('fetch', '--all')

    def get_remote_branches(self) -> list[str]:
        output = self.run('branch', '-r').splitlines()
        return [r.replace('*', '').strip() for r in output]

    def get_local_branches(self) -> list[str]:
        output = self.run('branch').splitlines()
        return [r.replace('*', '').strip() for r in output]

    def get_tags(self) -> list[str]:
        return self.run('tag').splitlines()
