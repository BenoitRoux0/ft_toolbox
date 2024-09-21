import os
import sys

def create_alias():
    shell_var = os.environ.get("SHELL", "")
    home_dir = os.path.expanduser("~")

    if "bash" in shell_var:
        config_file = os.path.join(home_dir, ".bashrc")
    elif "zsh" in shell_var:
        config_file = os.path.join(home_dir, ".zshrc")
    else:
        print("Unknown shell. The 'alias' command works with bash and zsh only.")
        sys.exit(1)

    if not os.path.exists(config_file):
        print(f"{config_file} not found")
        sys.exit(1)

    alias_line = "alias fttb='python3 -m fttb'\n"

    try:
        with open(config_file, "r") as file:
            content = file.read()
            if alias_line in content:
                print("Alias already exists in the config file.")
                return

        with open(config_file, "a") as file:
            file.write(f"\n{alias_line}")
        print(f"Alias created in {config_file}. You can now use the 'fttb' command after restarting your shell or running 'source {config_file}'.")
    except PermissionError:
        print(f"Permission denied when trying to write to {config_file}. Try running the script with sudo.")
        sys.exit(1)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
        sys.exit(1)
