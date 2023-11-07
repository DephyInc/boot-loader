.. _bootloader_quickstart:

Quickstart
==========

.. note::
   **TL;DR** Use ``bootloader list`` to view all of the available commands. You can then
   use ``booloader <command> --help`` to view the documentation for that command.

After installing ``bootloader`` as described `here <bootloader_docs_installing>`_, you
should have access to a command-line utility called ``bootloader``. You can check via:

.. code-block:: bash

   bootloader --version

If this command prints a version, you're good to go.

The primary function of the bootloader is to load new firmware onto Dephy's devices.
Each device has the following three microcontrollers on it:

* Mange (mn)
* Execute (ex)
* Regulate (re)

In addition to these three, each device has a bluetooth (bt121) module.

If your device is an exo (**not** an actpack), then it will have two additional
modules:

* Habsolute (habs; this is a Hall Effect sensor)
* XBee

``bootloader`` provides commands for flashing each of these.


Displaying Available Information
--------------------------------
``bootloader`` can require a lot of information. To help you navigate the available
options for certain fields, such as device name and rigid version, ``bootloader`` provides
the ``show`` command.

* ``bootloader show versions`` - Lists all available firmware versions
* ``bootloader show devices`` - Lists all devices for which there is firmware
* ``bootloader show rigids`` - Lists all rigid versions for which there is firmware
* ``bootloader show configs`` - Displays the available pre-made configurations for flashing

.. note::
   Not all combinations of device name, rigid version, and firmware version are supported

Flashing Regulate
-----------------

.. code-block:: bash

   bootloader flash re [options] <port> <current mn firmware> <to> <rigid version> <led>

Arguments:
  * port                     Port the device is on, e.g., `COM3`.
  * currentMnFw              Manage's current firmware, e.g., `7.2.0`.
  * to                       Version to flash, e.g., `9.1.0`, or path to file to use.
  * rigidVersion             PCB hardware version, e.g., `4.1B`.
  * led                      Either 'mono', 'multi', or 'stealth'

Options:
  * -b, --baudRate=BAUDRATE  Device baud rate. [default: 230400]
  * -l, --libFile=LIBFILE    C lib for interacting with Manage.
  * -h, --help               Display help for the given command. When no command is given display help for the list command.
  * -q, --quiet              Do not output any message.
  * -V, --version            Display this application version.
  *     --ansi               Force ANSI output.
  *     --no-ansi            Disable ANSI output.
  * -n, --no-interaction     Do not ask any interactive question.
  * -t, --theme=THEME        Sets theme.
  *     --debug              Enables tracebacks.
  * -v|vv|vvv, --verbose     Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.

If your device is an actpack then you will probably want ``led`` to be ``multi``
(indicating multiple colors will be used on the device's LED). If you are flashing an
exo, you will probably want ``led`` to be ``mono`` (indicating that the device's LED
will only use a single color).

.. note::
   The port can be determined by looking uder the COM Ports section of the Windows
   Device Manager.

.. note::
   The value of ``to`` can be either a semantic version string or a path to a file.
   If you are trying to use a semantic version string, e.g., 10.7.0, you will need
   AWS access keys in order to download the firmware. If these were not provided to
   you with your purchase, please reach out to Dephy at ``support@dephy.com``.

Example
+++++++

Let's we have an actpack currently running version 7.2.0 of the firmware, is connected
to port ``COM3``, and has a PCB version of ``4.1B`` and we want to flash version 10.7.0
of the firmware. If we have AWS access keys:

.. code-block:: bash

   bootloader flash re COM3 7.2.0 10.7.0 4.1B multi

If you do not have AWS access keys but do have a local 10.7.0 firmware file located at
``~/firmware/fw.cyacd``:

.. code-block:: bash

   bootloader flash re COM3 7.2.0 ~/firmware/fw.cyacd 4.1B multi

.. note::
   Only use firmware files given to you directly by Dephy or downloaded directly from
   the Dephy AWS firmware bucket.

Flashing Execute
----------------

.. code-block:: bash

   bootloader flash ex [options] <port> <current mn firmware> <to> <rigid version> <motor type>

Arguments:
  * port                     Port the device is on, e.g., `COM3`.
  * currentMnFw              Manage's current firmware, e.g., `7.2.0`.
  * to                       Version to flash, e.g., `9.1.0`, or path to file to use.
  * rigidVersion             PCB hardware version, e.g., `4.1B`.
  * motorType                Either 'actpack', 'dephy', or '61or91'

Options:
  * -b, --baudRate=BAUDRATE  Device baud rate. [default: 230400]
  * -l, --libFile=LIBFILE    C lib for interacting with Manage.
  * -h, --help               Display help for the given command. When no command is given display help for the list command.
  * -q, --quiet              Do not output any message.
  * -V, --version            Display this application version.
  *     --ansi               Force ANSI output.
  *     --no-ansi            Disable ANSI output.
  * -n, --no-interaction     Do not ask any interactive question.
  * -t, --theme=THEME        Sets theme.
  *     --debug              Enables tracebacks.
  * -v|vv|vvv, --verbose     Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.

If your device is a geared actpack, you will want ``motor type`` to be ``61or91``.

.. note::
   The port can be determined by looking uder the COM Ports section of the Windows
   Device Manager.

.. note::
   The value of ``to`` can be either a semantic version string or a path to a file.
   If you are trying to use a semantic version string, e.g., 10.7.0, you will need
   AWS access keys in order to download the firmware. If these were not provided to
   you with your purchase, please reach out to Dephy at ``support@dephy.com``.

Example
+++++++

Let's we have an actpack currently running version 7.2.0 of the firmware, is connected
to port ``COM3``, and has a PCB version of ``4.1B`` and we want to flash version 10.7.0
of the firmware. If we have AWS access keys:

.. code-block:: bash

   bootloader flash ex COM3 7.2.0 10.7.0 4.1B actpack

If you do not have AWS access keys but do have a local 10.7.0 firmware file located at
``~/firmware/fw.cyacd``:

.. code-block:: bash

   bootloader flash ex COM3 7.2.0 ~/firmware/fw.cyacd 4.1B actpack

.. note::
   Only use firmware files given to you directly by Dephy or downloaded directly from
   the Dephy AWS firmware bucket.

Flashing Manage
---------------
.. code-block:: bash

    flash mn [options] [--] <port> <currentMnFw> <to> <rigidVersion> <deviceName> <side>

Arguments:
  * port                     Port the device is on, e.g., `COM3`.
  * currentMnFw              Manage's current firmware, e.g., `7.2.0`.
  * to                       Version to flash, e.g., `9.1.0`, or path to file to use.
  * rigidVersion             PCB hardware version, e.g., `4.1B`.
  * deviceName               Name of the device, e.g., actpack.
  * side                     left, right, or none.

Options:
  * -b, --baudRate=BAUDRATE  Device baud rate. [default: 230400]
  * -l, --libFile=LIBFILE    C lib for interacting with Manage.
  * -h, --help               Display help for the given command. When no command is given display help for the list command.
  * -q, --quiet              Do not output any message.
  * -V, --version            Display this application version.
  *     --ansi               Force ANSI output.
  *     --no-ansi            Disable ANSI output.
  * -n, --no-interaction     Do not ask any interactive question.
  * -t, --theme=THEME        Sets theme.
  *     --debug              Enables tracebacks.
  * -v|vv|vvv, --verbose     Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.

Example
+++++++

Let's we have an actpack currently running version 7.2.0 of the firmware, is connected
to port ``COM3``, and has a PCB version of ``4.1B`` and we want to flash version 10.7.0
of the firmware. If we have AWS access keys:

.. code-block:: bash

   bootloader flash mn COM3 7.2.0 10.7.0 4.1B actpack none

If you do not have AWS access keys but do have a local 10.7.0 firmware file located at
``~/firmware/fw.cyacd``:

.. code-block:: bash

   bootloader flash ex COM3 7.2.0 ~/firmware/fw.cyacd 4.1B actpack

.. note::
   Only use firmware files given to you directly by Dephy or downloaded directly from
   the Dephy AWS firmware bucket.


Configurations
--------------

.. note::
   These commands are for internal-use by Dephy. However, they could be adapted to use your cloud storage

Configurations are sets of firmware files that go together, such as firmware version 7.2.0 for Mn, Ex, and Re
on an actpack. They can also refer to sets of files used in a particular experiment or at a
particular event. Rather than have to track these files indivudally, ``bootloader`` provides
a way to package these files together and upload them to the cloud for later use.

A configuration can be created via

.. code-block:: bash

   bootloader config create <configName>

You will then be prompted to enter the path to each firmware file you want to include in the configuration.
These files will be zipped together into an archive.

You can then upload the newly created archive with

.. code-block:: bash

   bootloader config upload <archiveName>

Download one with
.. code-block:: bash

   bootloader config download <archiveName>

and flashed with

.. code-block:: bash

   bootloader flash config [options] <port> <currentMnFw> <configName>

Arguments:
* port: Port the device is on, e.g., ``COM3``
* currentMnFw: Manage's current firmware, e.g., 7.2.0
* configName: Name of the configuration to use
