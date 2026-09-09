from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


CONFIG_FILE = "quarto-extensions.yml"


def run(*args: str, cwd: Path | None = None) -> None:
    print(f"> {' '.join(args)}")
    subprocess.run(args, cwd=cwd, check=True)


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        sys.exit(
            f"\nERROR: '{name}' was not found on PATH.\n"
            f"Install {name} and run this setup script again.\n"
        )


def load_plugins(config_path: Path) -> list[dict[str, str]]:
    if not config_path.exists():
        sys.exit(
            f"\nERROR: configuration file not found:\n"
            f"  {config_path}\n"
        )

    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or "plugins" not in data:
        sys.exit(
            f"\nERROR: '{CONFIG_FILE}' must contain a 'plugins:' list.\n"
        )

    plugins = data["plugins"]

    if not isinstance(plugins, list):
        sys.exit(
            f"\nERROR: 'plugins' in '{CONFIG_FILE}' must be a list.\n"
        )

    normalized: list[dict[str, str]] = []

    for i, plugin in enumerate(plugins, start=1):
        if not isinstance(plugin, dict):
            sys.exit(
                f"\nERROR: plugin entry #{i} must be a mapping.\n"
            )

        name = plugin.get("name")
        repo = plugin.get("repo")
        path = plugin.get("path")
        ref = plugin.get("ref", "HEAD")

        if not name or not repo or not path:
            sys.exit(
                f"\nERROR: plugin entry #{i} must contain:\n"
                "  name:\n"
                "  repo:\n"
                "  path:\n"
            )

        normalized.append(
            {
                "name": str(name),
                "repo": str(repo),
                "ref": str(ref),
                "path": str(path),
            }
        )

    return normalized


def clone_or_update_plugin(
    plugin: dict[str, str],
    private_root: Path,
) -> Path:
    name = plugin["name"]
    repo = plugin["repo"]
    ref = plugin["ref"]

    plugin_repo = private_root / name

    if not plugin_repo.exists():
        print(f"\nDownloading plugin: {name}")

        try:
            clone_args = [
                "git",
                "clone",
                "--depth",
                "1",
            ]

            if ref != "HEAD":
                clone_args.extend(
                    [
                        "--branch",
                        ref,
                        "--single-branch",
                    ]
                )

            clone_args.extend(
                [
                    repo,
                    str(plugin_repo),
                ]
            )

            run(*clone_args)
        except subprocess.CalledProcessError:
            sys.exit(
                f"\nERROR: could not clone plugin '{name}'.\n\n"
                f"Repository:\n"
                f"  {repo}\n\n"
                "Make sure your GitHub account has access and that "
                "Git authentication is configured on this machine."
            )

    else:
        print(f"\nUpdating plugin to newest version: {name}")

        try:
            run(
                "git",
                "-C",
                str(plugin_repo),
                "fetch",
                "--depth",
                "1",
                "origin",
                ref,
            )
            run(
                "git",
                "-C",
                str(plugin_repo),
                "checkout",
                "--detach",
                "--force",
                "FETCH_HEAD",
            )
        except subprocess.CalledProcessError:
            sys.exit(
                f"\nERROR: could not update plugin '{name}'.\n"
            )
            
    return plugin_repo


def install_plugin(
    plugin: dict[str, str],
    plugin_repo: Path,
    project_root: Path,
) -> None:
    name = plugin["name"]

    source_extension = plugin_repo / plugin["path"]
    installed_extension = project_root / "_extensions" / name

    if not source_extension.exists():
        sys.exit(
            f"\nERROR: extension path not found for '{name}':\n"
            f"  {source_extension}\n"
        )

    extension_yml = source_extension / "_extension.yml"

    if not extension_yml.exists():
        sys.exit(
            f"\nERROR: '{source_extension}' does not look like "
            "a Quarto extension.\n\n"
            "Expected:\n"
            f"  {extension_yml}\n"
        )

    if installed_extension.exists():
        print(f"\nRemoving previous installed extension: {name}")
        shutil.rmtree(installed_extension)

    print(f"\nInstalling Quarto extension: {name}")
    print(f"  source: {source_extension}")

    # Quarto expects an extension distribution root containing:
    #
    #   _extensions/
    #       extension-name/
    #
    # We therefore stage only the requested extension in a temporary
    # distribution directory. This prevents other extensions contained
    # in the same private repository from being installed accidentally.
    with tempfile.TemporaryDirectory(prefix="quarto-extension-") as tmp:
        staging_root = Path(tmp)

        staging_extension = (
            staging_root
            / "_extensions"
            / name
        )

        staging_extension.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copytree(
            source_extension,
            staging_extension,
        )

        try:
            run(
                "quarto",
                "add",
                str(staging_root),
                "--no-prompt",
                cwd=project_root,
            )
        except subprocess.CalledProcessError:
            sys.exit(
                f"\nERROR: Quarto could not install extension '{name}'.\n"
            )

    if not installed_extension.exists():
        sys.exit(
            f"\nERROR: '{name}' was not found after installation at:\n"
            f"  {installed_extension}\n"
        )


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    config_path = project_root / CONFIG_FILE
    private_root = project_root / ".private-extensions"

    print("Project:")
    print(f"  {project_root}")

    print("\nChecking required tools...")
    require_command("git")
    require_command("quarto")

    print("\nReading extension configuration:")
    print(f"  {config_path}")

    plugins = load_plugins(config_path)

    if not plugins:
        print("\nNo extensions configured.")
        return

    private_root.mkdir(exist_ok=True)

    print(f"\nConfigured plugins: {len(plugins)}")

    for plugin in plugins:
        print(
            f"  - {plugin['name']} "
            f"({plugin['path']}, ref: {plugin['ref']})"
        )

    for plugin in plugins:
        plugin_repo = clone_or_update_plugin(
            plugin,
            private_root,
        )

        install_plugin(
            plugin,
            plugin_repo,
            project_root,
        )

    print("\nInstalled Quarto extensions:")
    run(
        "quarto",
        "list",
        "extensions",
        cwd=project_root,
    )

    print("\nSetup complete.")
    print("\nYou can now run:")
    print("  quarto preview")


if __name__ == "__main__":
    main()
