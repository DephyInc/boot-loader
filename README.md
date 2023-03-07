# Dephy Bootloader

This is a tool for loading firmware onto Dephy's devices.

## AWS Access

A pre-compiled C library in order to communicate with your device.
These libraries are hosted in a public AWS S3 bucket called `dephy-public-binaries`.
Use the `show` command to view the available versions (see below).

Additionally, you will need a firmware file (or files) to put on your device. These
files are hosted in a private AWS S3 bucket. You should have received access keys as
a part of your purchase. If you did not, please contact `support@dephy.com`.

Once you receive your keys, you'll need to store them in a credentials file to be read
by `boto3` (the Python module for interacting with S3).

```bash
mkdir ~/.aws
touch ~/.aws/credentials # Note that there is no extension!
```

Edit the credentials file to contain the following:

```bash
[default]
aws_access_key_id=<YOUR ACCES KEY ID HERE>
aws_secret_access_key=<YOUR SECRET ACCESS KEY HERE>

[dephy]
aws_access_key_id=<YOUR ACCES KEY ID HERE>
aws_secret_access_key=<YOUR SECRET ACCESS KEY HERE>
```

**NOTE**: If you already have an S3 account, you'll want to put those keys under `default`
and the Dephy keys under `dephy`. If your Dephy access keys are the only ones you have,
you'll want to put the same keys in both sections. `boto3` will fail if it does not
find a `default` section, but the bootloader explicitly looks for a `dephy` section in
case you have other keys.

## Installation

It is **highly recommended**, but not required, that you install `bootloader` in a virtual
environment. This helps keep your python and associated packages sandboxed from the
rest of your system and, potentially, other versions of the same packages required by
`bootloader`.

You can create a virtual environment via (these commands are for Linux. See the **NOTE**
below for Windows):

```bash
mkdir ~/.venvs
python3 -m venv ~/.venvs/dephy
```

Activate the virtual environment with:

```bash
source ~/.venvs/dephy/bin/activate
```

**NOTE**: If you're on Windows, the activation command is: `source ~/.venvs/dephy/Scripts/activate`.
Additionally, replace `python3` with `python`.


### From PyPI

This is the simplest installation method. 

```bash
python3 -m pip install dephy-bootloader
```

### From Source

To install from source:

```bash
git clone https://github.com/DephyInc/boot-loader.git
cd boot-loader/
git checkout main # Or whichever branch you're interested in
python3 -m pip install .
```

## Drivers

Bootloading one of Dephy's devices requires communicating with the microcontroller
called Manage. Manage is a stm32 chip, which means that the stm32 drivers are needed
in order for the bootloader to function correctly. The easiest way to install these
drivers is to run the installer for the STM32 ST-Link Utility, which can be found
[here](https://www.st.com/en/development-tools/stsw-link004.html#tools-software).
Once the installation of the STM32 ST-Link Utility finishes, it should prompt you to
install the device drivers. 


## Usage

This package provides the `bootload` command-line tool. To see the available commands,
simply run `bootload --help`. Additionally, each subcommand has a `--help` option
that will give you more information on its usage.
