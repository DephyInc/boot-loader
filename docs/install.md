# Installation


## System Requirements

* Windows
    * The bootloader wraps several third-party tools, some of which are only compatible
    with Windows, which is why the bootloader does not work on other operating systems
* Python 3.11
* STM Drivers
    * The easiest way to get these is to install the STM programmer from
    [here](https://www.st.com/en/development-tools/stm32cubeprog.html). Once installed,
    the installation wizard should prompt you to install the drivers. Select yes.
* Proper AWS credentials
    * Dephy's firmware is stored on AWS' S3 cloud storage service, and downloading the
    firmware requires access keys. These keys should have been provided to you when
    you purchased your device. If not, please reach out to through the form [here](https://dephy.com/faster/)
    * If you already have a valid Dephy firmware file you'd like to flash then you do
    not need access keys
    * Your access keys need to be saved in `~/.aws/credentials` in a section called `[dephy]`. See [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#shared-credentials-file)


## Installation

It is strongly recommended that you install `bootloader` in a virtual environment (the commands below assume you are using the [Git Bash Terminal](https://git-scm.com/download/win))
```python
mkdir ~/.venvs
python -m venv ~/.venvs/dephy
source ~/.venvs/dephy/Scripts/activate
```

Then install from PyPI
```python
python -m pip install bootloader
```
