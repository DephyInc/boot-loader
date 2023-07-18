# Commands

The commands below are presented in alphabetical order.
    

## Config

These commands are related to creating and using bundles of firmware files that are 
commonly used together. Please note that these commands are for internal Dephy use only
and will not work without the proper credentials.

### config create
```bash
bootloader config create <configName> [--mn-file=] [--ex-file=] [--re-file=] [--habs-file=] [--firmware-version=]
```

Creates a bundle of firmware files with the name `configName`.
* `--mn-file=` : Option to specify the firmware file for Manage. If not given, the command will prompt you for a file to use
* `--ex-file=` : Option to specify the firmware file for Execute. If not given, the command will prompt you for a file to use
* `--re-file=` : Option to specify the firmware file for Regulate. If not given, the command will prompt you for a file to use
* `--habs-file=` : Option to specify the firmware file for Habsolute. If not given, the command will prompt you for a file to use
* `--firmware-version=` : In order to interact with a device, we need to know which version of the API the firmware uses. That version is specified with this option. If not given, the command will prompt you for the version 

## Flash

These commands are used to load new firmware onto Dephy's devices. There are three
microcontrollers: Manage (mn), Execute (ex), and Regulate (re). There are two radios:
bluetooth (bt121) and xbee. There is one Hall effect sensor: Habsolute (habs).

### flash all
```bash
bootloader flash all <port> <currentMnFirmware> [--to=] [--rigidVersion=] [--device=] [--side=] [--motorType=] [--led=] [--address=] [--level=] [--buddyAddress=] [--baudRate=230400] [--libFile=]
```

Flashes each target with a **local** firmware file (i.e., not cached on S3).
* `port` : The COM port the device is connected to 
* `currentMnFirmware` : Semantic version string for the firmware currently on Manage. Needed for communication with the device
* `--to` : Option specifying the semantic version string of the firmware you'd like to flash. This is only for ex, mn, re, and habs. If not given, the command will prompt you
* `--rigidVersion` : Option specifying the hardware version of the device, e.g., 4.1B. If not given, the command will prompt you
* `--device` : Option specifying the type of the device, e.g., actpack. If not given, the command will prompt you
* `--side` : Option specifying left, right, or none. If not given, the command will prompt you
* `--motorType` : Option specifying the motor type; 'actpack', 'exo', or '61or91'. If not given, the command will prompt you
* `--led` : Option specifying the LED pattern to use; 'mono', 'multi', or 'stealth'. If not given, the command will prompt you
* `--address` : Option specifying Bluetooth address. If not given, the command will prompt you
* `--level` : Option specifying Gatt level to use. If not given, the command will prompt you
* `--buddyAddress` : Option specifying Bluetooth address of device's buddy. If not given, the command will prompt you
* `--baudRate` : Option specifying the baud rate. If not given, the default value of 230400 will be used
* `--libFile` : Option specifying the C library for interacting with Manage. If not given, the command will prompt you

### flash bt121
```bash
bootloader flash bt121 <port> <currentMnFirmware> <address> <level> [--baudRate=230400] [--libFile=]
```

Flashes new firmware onto the bluetooth radio.
* `port` : The COM port the device is connected to 
* `currentMnFirmware` : Semantic version string for the firmware currently on Manage. Needed for communication with the device
* `address` : Bluetooth address
* `level` : Gatt level to use
* `--baudRate` : Option specifying the baud rate. If not given, the default value of 230400 will be used
* `--libFile` : Option specifying the C library for interacting with Manage

### flash ex
```bash
bootloader flash ex <port> <currentMnFirmware> <to> <rigidVersion> <motorType> [--baudRate=230400] [--libFile=]
```

Flashes new firmware onto Execute.
* `port` : The COM port the device is connected to 
* `currentMnFirmware` : Semantic version string for the firmware currently on Manage. Needed for communication with the device
* `to` : **Either** the semantic version string of the firmware you'd like to flash (e.g., 7.2.0) **OR** the path to a local firmware file you'd like to use
* `rigidVersion` : Hardware version of the device, e.g., 4.1B
* `motorType` : Motor type; 'actpack', 'exo', or '61or91'
* `--baudRate` : Option specifying the baud rate. If not given, the default value of 230400 will be used
* `--libFile` : Option specifying the C library for interacting with Manage

### flash habs
```bash
bootloader flash habs <port> <currentMnFirmware> <to> [--baudRate=230400] [--libFile=]
```

Flashes new firmware onto Habsolute.
* `port` : The COM port the device is connected to 
* `currentMnFirmware` : Semantic version string for the firmware currently on Manage. Needed for communication with the device
* `to` : **Either** the semantic version string of the firmware you'd like to flash (e.g., 7.2.0) **OR** the path to a local firmware file you'd like to use
* `--baudRate` : Option specifying the baud rate. If not given, the default value of 230400 will be used
* `--libFile` : Option specifying the C library for interacting with Manage

### flash mn
```bash
bootloader flash mn <port> <currentMnFirmware> <to> <rigidVersion> <deviceName> <side> [--baudRate=230400] [--libFile=]
```

Flashes new firmware onto Manage.
* `port` : The COM port the device is connected to 
* `currentMnFirmware` : Semantic version string for the firmware currently on Manage. Needed for communication with the device
* `to` : **Either** the semantic version string of the firmware you'd like to flash (e.g., 7.2.0) **OR** the path to a local firmware file you'd like to use
* `rigidVersion` : Hardware version of the device, e.g., 4.1B
* `device` : Type of the device, e.g., actpack
* `side` : Left, right, or none
* `--baudRate` : Option specifying the baud rate. If not given, the default value of 230400 will be used
* `--libFile` : Option specifying the C library for interacting with Manage

### flash re
```bash
bootloader flash re <port> <currentMnFirmware> <to> <rigidVersion> <led> [--baudRate=230400] [--libFile=]
```

Flashes new firmware onto Regulate.
* `port` : The COM port the device is connected to 
* `currentMnFirmware` : Semantic version string for the firmware currently on Manage. Needed for communication with the device
* `to` : **Either** the semantic version string of the firmware you'd like to flash (e.g., 7.2.0) **OR** the path to a local firmware file you'd like to use
* `rigidVersion` : Hardware version of the device, e.g., 4.1B
* `led` : LED pattern to use; 'mono', 'multi', or 'stealth'
* `--baudRate` : Option specifying the baud rate. If not given, the default value of 230400 will be used
* `--libFile` : Option specifying the C library for interacting with Manage

### flash xbee
```bash
bootloader flash xbee <port> <currentMnFirmware> <address> <buddyAddress> [--baudRate=230400] [--libFile=]
```

Flashes new firmware onto Xbee.
* `port` : The COM port the device is connected to 
* `currentMnFirmware` : Semantic version string for the firmware currently on Manage. Needed for communication with the device
* `address` : Bluetooth address
* `buddyAddress` : Bluetooth address of device's buddy
* `--baudRate` : Option specifying the baud rate. If not given, the default value of 230400 will be used
* `--libFile` : Option specifying the C library for interacting with Manage

### flash config
```bash
bootloader flash config <port> <currentMnFirmware> <configName> [--baudRate=230400] [--libFile=]
```

Flashes new firmware onto Xbee.
* `port` : The COM port the device is connected to 
* `currentMnFirmware` : Semantic version string for the firmware currently on Manage. Needed for communication with the device
* `configName` : Name of the configuration to use 
* `--baudRate` : Option specifying the baud rate. If not given, the default value of 230400 will be used
* `--libFile` : Option specifying the C library for interacting with Manage


## Show

### show configs
```bash
bootloader show configs
```

Lists the names of the available configurations to flash. Can only be used internally by Dephy.
