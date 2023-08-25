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
  * motorType                Either 'actpack', 'exo', or '61or91'

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
