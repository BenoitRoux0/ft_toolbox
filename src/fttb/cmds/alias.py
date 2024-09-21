import os

def create_alias():
	shell_var = os.getenv("SHELL")
	if shell_var == "/bin/bash":
		config_file = "/.bashrc"
	elif shell_var == "/bin/zsh":
		config_file = "/.zshrc"
	else:
		print("Unknown shell, command \"alias\" works with bash and zsh only")
		exit()
	if not os.path.exists(f"{os.getenv('HOME')}{config_file}"):
		print(f"{os.getenv('HOME')}{config_file} not found")
		exit()

	with open(f"{os.getenv('HOME')}{config_file}",) as file:
			file.write("alias fttb='python3.10 -m fttb'")
	print("Alias created, you can now use \"fttb\" command")
	exit()

