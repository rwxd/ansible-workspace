from ansible_workspace.cli import app


def main() -> int:
    app()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
