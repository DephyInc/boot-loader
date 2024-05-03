.. _bootloader_troubleshooting:

Troubleshooting
===============


Bootloader Aborts for Seemingly No Reason
-----------------------------------------

This is a common occurance in some Windows terminals. The **TL;DR** is that you should
use the ``--no-interaction`` option on the command you are trying to run.

The longer explanation is that, under the hood, ``bootloader`` uses `cleo <https://cleo.readthedocs.io/en/latest/index.html>`_ to help build out its command-line interface.
There's a `bug <https://github.com/python-poetry/cleo/issues/333>`_ in cleo where,
when calling one command from another, if the command being called uses ``confirm``,
then ``_stream`` isn't set, which causes a no attribute error. This causes
``bootloader`` to assume the default option, which, for safety's sake, is ``no``.
This, in turn, causes ``bootloader`` to abort the present operation.

By using the ``no-interaction`` option, ``bootloader`` will skip these confirmation
checks. This has the advantage of allowing the operation to proceed, but the
disadvantage of not allowing the user to double check their input before proceeding,
so please be careful and check your input before running the command!


Cannot Connect to Manage Once it is in Tunnel Mode
--------------------------------------------------

There was a bug in the documentation in a previous version of ``bootloader`` that
linked to incorrect drivers for a DFU device. As such, without the correct drivers,
your computer does not know how to talk to Manage once it has been switched into
DFU mode.

Newer versions of ``bootloader`` (>=2.1), download and install the correct drivers
for you. However, if the incorrect drivers are already installed, they may need to
be manually removed before the new ones will work.

You'll want to follow the instructions given `here <https://www.winhelponline.com/blog/driver-uninstall-completely-windows/#pnputil>`_ to remove the currently installed STM drivers. Please double check you are removing the correct drivers before proceeding!


DfuSe Command Fails
-------------------

Under the hood, ``bootloader`` employs several third-party tools in order to
communicate with the microcontrollers on the device. One of these tools is called
``DfuSeCommand.exe`` and is provided by ST. One reason that the tool may fail is
because it cannot find one or more required libraries. While these libraries should
all be provided by the version of ``DfuSeCommand`` bundled with ``bootloader``, if
they are missing or cannot be found for any reason, the simplest approach is to
run the official installer provided by ST, which can be found [here](https://www.st.com/en/development-tools/stsw-stm32080.html).
