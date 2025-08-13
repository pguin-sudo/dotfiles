#!/usr/bin/env python3
import argparse
import logging
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class DotfilesManager:
    def __init__(self):
        self.home = Path.home()
        self.base_dir = Path(".").absolute()
        self.configs_dir = self.base_dir / "configs"
        self.host_config = self._load_host_config()
        self.config = {
            "assume_yes": False,
            "force": False,
            "dry_run": False,
        }

    def _load_host_config(self) -> dict:
        """Load host configuration from hosts"""
        host_file = self.base_dir / "hosts" / f"{socket.gethostname()}.yaml"
        if not host_file.exists():
            logger.error(f"❌ Configuration file not found: {host_file}")
            sys.exit(1)

        try:
            with open(host_file, "rb") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"❌ Error loading {host_file}: {e}")
            sys.exit(1)

    def _prompt_yes_no(self, question: str, default: bool = None) -> bool:
        """Prompt user for yes/no input"""
        if self.config["assume_yes"]:
            logger.info(f"{question} [auto-accepted]")
            return True

        choices = "Y/n" if default else "y/N" if default is not None else "y/n"
        reply = input(f"{question} [{choices}] ").strip().lower()
        if not reply and default is not None:
            return default
        return reply in ("y", "yes")

    def _is_package_installed(self, pkg_name: str) -> bool:
        """Check if package is installed"""
        try:
            subprocess.run(
                ["pacman", "-Qi", pkg_name],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def install_packages(self):
        """Install packages listed in YAML"""
        packages = self.host_config.get("packages", [])
        if not packages:
            logger.info("ℹ️ No packages to install")
            return True

        logger.info("📦 Packages to install:")
        to_install = []
        for pkg in packages:
            name = pkg.get("name")
            if not name:
                continue

            if self._is_package_installed(name):
                logger.info(f"ℹ️ {name} already installed")
                continue

            if self._prompt_yes_no(f"Install {name}?", default=True):
                to_install.append(name)

        if not to_install:
            logger.info("⏩ No packages selected for installation")
            return True

        if self.config["dry_run"]:
            logger.info(f"DRY RUN: Would install: {' '.join(to_install)}")
            return True

        if any(any(char.isspace() for char in pkg) for pkg in to_install):
            logger.debug("Splitting multi-name packages...")

        to_install = [part for pkg in to_install for part in pkg.split()]

        use_yay = bool(shutil.which("yay"))
        for pkg in to_install:
            try:
                cmd = (
                    ["yay", "-S", "--needed", "--noconfirm", pkg]
                    if use_yay
                    else ["sudo", "pacman", "-S", "--needed", "--noconfirm", pkg]
                )

                logger.info(f"Installing {pkg}...")
                subprocess.run(cmd, check=True)
                logger.info(f"✅ Installed {pkg}")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install {pkg}: {e}")
                return False
        return True

    def _create_symlink(self, src: Path, dest: Path):
        """Create a symlink with overwrite handling"""
        if not src.exists():
            logger.error(f"Source does not exist: {src}")
            return False

        if dest.is_symlink() and dest.resolve() == src:
            logger.info(f"🔗 Link {dest} already exists")
            return True

        if dest.exists() or dest.is_symlink():
            if not self.config["force"] and not self._prompt_yes_no(
                f"Overwrite {dest}?", default=False
            ):
                return True

            if dest.is_symlink():
                dest.unlink()
            else:
                backup = dest.with_name(dest.name + ".bak")
                dest.rename(backup)
                logger.info(f"💾 Backed up to {backup}")

        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(src, dest)
            logger.info(f"🔗 Created: {dest} → {src}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to link {src} → {dest}: {e}")
            return False

    def create_symlinks(self):
        """Create symlinks for config files"""
        packages = self.host_config.get("packages", [])
        if not packages:
            logger.info("ℹ️ No packages with configs")
            return True

        success = True
        for pkg in packages:
            name = pkg.get("name")
            config = pkg.get("config")
            if not config:
                continue

            src_base = self.configs_dir
            pattern = config.strip()

            matches = (
                list(src_base.glob(pattern)) if "*" in pattern else [src_base / pattern]
            )

            if not matches:
                logger.warning(f"⚠️ No files match: {src_base}/{pattern}")
                continue

            for src in matches:
                if not src.exists():
                    logger.warning(f"⚠️ Config not found: {src}")
                    continue

                rel_path = src.relative_to(src_base)
                dest = self.home / rel_path

                if self.config["dry_run"]:
                    logger.info(f"DRY RUN: Would link {src} → {dest}")
                    continue

                if not self._create_symlink(src, dest):
                    success = False

        return success

    def run_setup_commands(self):
        """Run setup commands for packages"""
        packages = self.host_config.get("packages", [])
        if not packages:
            return True

        success = True
        for pkg in packages:
            if "setup" not in pkg:
                continue

            if not self._is_package_installed(pkg["name"]):
                logger.warning(f"⚠️ {pkg['name']} not installed, skipping setup")
                continue

            if "check" in pkg:
                cmd = pkg["check"]["cmd"]
                result = pkg["check"]["result"]

                try:
                    logger.debug(f"⚙️ Running check: {cmd}")
                    cmd_result = subprocess.run(
                        cmd,
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    if cmd_result.stdout == result:
                        logger.debug(f"✅ Check completed for {pkg['name']}")
                        continue
                except Exception as e:
                    logger.debug(f"❌ Check failed for {pkg['name']}: {e}")
                    success = False
                    continue

                logger.debug(f"✅ Setup for {pkg['name']} has been already run")

            cmd = pkg["setup"]["cmd"]
            if self.config["dry_run"]:
                logger.info(f"DRY RUN: Would run: {cmd}")
                continue

            try:
                logger.info(f"⚙️ Running setup: {cmd}")
                subprocess.run(cmd, shell=True, check=True)
                logger.info(f"✅ Setup completed for {pkg['name']}")
            except Exception as e:
                logger.error(f"❌ Setup failed for {pkg['name']}: {e}")
                success = False
        return success

    def run(self):
        parser = argparse.ArgumentParser(description="Dotfiles Manager")
        parser.add_argument("--install", action="store_true", help="Install packages")
        parser.add_argument("--symlink", action="store_true", help="Create symlinks")
        parser.add_argument("--setup", action="store_true", help="Run setup commands")
        parser.add_argument("--all", action="store_true", help="Run all operations")
        parser.add_argument("--yes", action="store_true", help="Auto-confirm prompts")
        parser.add_argument("--dry-run", action="store_true", help="Preview changes")
        parser.add_argument("--force", action="store_true", help="Force overwrites")
        parser.add_argument("--verbose", action="store_true", help="Verbose execution")

        args = parser.parse_args()
        self.config.update(
            {
                "assume_yes": args.yes,
                "force": args.force,
                "dry_run": args.dry_run,
            }
        )

        if args.verbose:
            logger.setLevel(logging.DEBUG)

        if not any(vars(args).values()):
            parser.print_help()
            return

        success = True
        if args.all or args.install:
            success &= self.install_packages()
        if args.all or args.symlink:
            success &= self.create_symlinks()
        if args.all or args.setup:
            success &= self.run_setup_commands()

        sys.exit(0 if success else 1)


if __name__ == "__main__":
    DotfilesManager().run()
