# Arch Linux Dotfiles Manager

A simple Python script to manage dotfiles installation and configuration on Arch Linux-based systems.

## Features

- Install packages from TOML configuration
- Create symlinks for configuration files
- Run post-install setup commands
- Dry-run mode for previewing changes
- Interactive prompts with auto-confirm option
- Conflict handling with backups

## Requirements

- Python 3.7+
- Arch Linux or derivative (Manjaro, EndeavourOS, etc.)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/pguin-sudo/dotfiles.git ~/.dotfiles
   cd ~/.dotfiles
   ```

[!WARNING]  
Do not delete repository after installization. It makes symlinks, which will be broken!

## Configuration

Edit `hosts/desktop.toml` to define your packages and configurations:

```toml
packages = [
    # Simple package
    { name = "git" },
    
    # Package with config
    { name = "helix", config = ".config/helix/*" },
    
    # Package with config and setup command
    { name = "fish", config = ".config/fish/*", setup = "chsh -s /usr/bin/fish" },
]
```

### Configuration Options

- `name`: Package name (required)
- `config`: Path to config file(s) in `./configs/` directory (supports glob patterns)
- `setup`: Post-install command to run

## Usage

```bash
# Install packages, create symlinks, and run setup commands
./manager.py --all

# Individual operations
./manager.py --install    # Install packages only
./manager.py --symlink    # Create symlinks only
./manager.py --setup      # Run setup commands only

# Additional options
./manager.py --all --dry-run  # Preview changes
./manager.py --all --yes      # Auto-confirm all prompts
./manager.py --symlink --force # Force overwrite existing files
```

## File Structure

```
dotfiles/
├── configs/                  # Your configuration files
│   ├── .gitconfig
│   └── .config/
│       ├── fish/
│       └── helix/
├── hosts/
│   └── desktop.toml          # Package definitions
├── manager.py       # This script
└── README.md                 # This file
```

## How It Works

1. **Package Installation**:
   - Checks if package is already installed
   - Uses `yay` if available, falls back to `pacman`
   - Interactive prompts by default

2. **Symlink Creation**:
   - Creates symlinks from `./configs/` to appropriate locations
   - Handles glob patterns (e.g., `*.conf`)
   - Creates parent directories as needed
   - Backs up existing files before overwriting

3. **Setup Commands**:
   - Runs post-install commands (e.g., `chsh`)
   - Only runs for installed packages

## Tips

1. Use `--dry-run` first to preview changes
2. Add `--yes` for unattended installation
3. Config paths are relative to `./configs/`:
   - `.gitconfig` → `./configs/.gitconfig`
   - `.config/helix/*` → `./configs/.config/helix/*`

MIT License. See [LICENSE](LICENSE) for details.
