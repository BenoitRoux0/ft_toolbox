# Ft_toolbox

A command-line interface to download JetBrains IDEs on computers within the 42 network.


## Installation

Install from pypi with pip

```bash
pip install fttb
```

After the install, we recommand to install the alias for ease of use :
```bash
python3 -m fttb alias
```

This allows you to use `fttb` as a command instead of `python3 -m fttb`.

## Features
- List all available JetBrains IDEs and their versions
- Download the latest version or a specific version of an IDE
- Automatically install IDEs in the correct folder and add a .desktop entry

## Usage/Examples
**Note:** The following examples assume you've set up the `fttb` alias. If not, use `python3 -m fttb <command>` instead.

### Configuration

Configure the tool with the following options:

```bash
fttb config [OPTIONS]
```

Options:
- `--cache-path CACHE_PATH`: Set download cache path
- `--install-path INSTALL_PATH`: Set IDEs installation path
- `--bin-path BIN_PATH`: Set IDEs binaries path

### Listing IDEs

List all available IDEs:

```bash
fttb list
```

List all available versions of a specific IDE:

```bash
fttb list <IDE_NAME>
```

### Downloading IDEs

Download the latest version of an IDE:

```bash
fttb use <IDE_NAME>
```

Download a specific version of an IDE:

```bash
fttb use <IDE_NAME> <VERSION>
```

### Clear download cache
```bash
fttb clear
```

## Author
#### Benoit Roux
> Core development and project managment
- Github: [@BenoitRoux0](https://github.com/BenoitRoux0)
### Guillaume d´Harcourt
> Features development and misc
- Github: [@gd-harco](https://github.com/gd-harco)

## Support
We welcome all feedback and suggestions. If you need help, have a feature request, or found a bug, please open a new issue on our GitHub repository.

You can also reach out to us on the 42_born2code Slack workspace.

## Current Limitations
Currently, the tool has only been tested at the 42 Lyon campus. We are not certain if it will work on other campuses, as we don't know how user environments are set up at other locations.

Please report any issues you encounter so that we can create the best tool possible for the entire 42 network.

### links
[pypi page](https://pypi.org/project/fttb/)

