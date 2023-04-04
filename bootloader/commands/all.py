from cleo.helpers import argument
from cleo.helpers import option

from bootloader.commands.base_command import BaseCommand


# ============================================
#              FlashAllCommand
# ============================================
class FlashAllCommand(BaseCommand):
    """
    Flashes bt121, xbee, habs, ex, re, and mn.
    """

    name = "all"
    description = "Flashes bt121, xbee, habs, ex, re, and mn."

    arguments = [
        argument("currentMnFw", "Current firmware version on Manage, e.g., `7.2.0`."),
        argument("to", "Desired firmware version, e.g., `9.1.0`, or firmware file."),
    ]

    options = [
        option("address", "-a", "BT address. Default is the device id.", flag=False),
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
        option("buddyAddress", None, "Address of device's buddy.", flag=False),
        option("deviceName", "-d", "Device to flash, e.g., `actpack`.", flag=False),
        option("libFile", "-l", "C lib for interacting with Manage.", flag=False),
        option("port", "-p", "Port the device is on, e.g., `COM3`.", flag=False),
        option("rigidVersion", "-r", "PCB hardware version, e.g., `4.1B`.", flag=False),
        option("side", "-s", "Either left or right.", flag=False),
        option("theme", None, "classic, light, dark, or none", flag=False),
    ]

    help = """
    Flashes bt121, xbee (if applicable), habs (if applicable), ex, re, and mn.

    For xbee and habs, there is currently no good way of determing whether or not
    a device has those chips, so this command will prompt you whether or not you
    want to flash those chipsself.

    If no arguments are given for the buddyAddress and you do wish to flash xbee,
    the command will prompt you for a value.

    Unlike other flash commands, here the `to` argument must be a semantic version
    string for a version hosted on S3. Use the `show-available` command to see
    what versions are available.

    # Examples
    > bootload all 7.2.0 9.1.0
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._currentMnFw: str = ""
        self._to: str = ""
        self._address: str = ""
        self._baudRate: int = -1
        self._buddyAddress: str = ""
        self._deviceName: str = ""
        self._level: int | None = None
        self._libFile: str = ""
        self._port: str = ""
        self._rigidVersion: str = ""
        self._side: str = ""

    # -----
    # handle
    # -----
    def handle(self) -> int:
        """
        Entry point for the command.
        """
        self._parse_options()
        self._setup()

        self._flash_bt121()
        self._flash_xbee()

        for target in ["habs", "ex", "re", "mn"]:
            self._flash_microcontroller(target)

        return 0

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        self._currentMnFw = self.argument("currentMnFw")
        self._to = self.argument("to")

        self._address = self.option("address")
        self._baudRate = self.option("baudRate")
        self._buddyAddress = self.option("buddyAddress")
        self._deviceName = self.option("deviceName")
        self._libFile = self.option("libFile")
        self._port = self.option("port")
        self._rigidVersion = self.option("rigidVersion")
        self._side = self.option("side")
        self._theme = self.option("theme")

    # -----
    # _flash_bt121
    # -----
    def _flash_bt121(self) -> None:
        # https://github.com/python-poetry/cleo/issues/130
        args = f"bt121 {self._currentMnFw} "

        # The default value of None will get passed as the string 'None' if we
        # just include each value
        if self._address:
            args += f"--address {self._address} "
        if self._baudRate:
            args += f"--baudRate {self._baudRate} "
        if self._level:
            args += f"--level {self._level} "
        if self._libFile:
            args += f"--libFile {self._libFile} "
        if self._port:
            args += f"--port {self._port} "
        if self._theme:
            args += f"--theme {self._theme} "

        self.call("bt121", args)

    # -----
    # _flash_xbee
    # -----
    def _flash_xbee(self) -> None:
        if not self.confirm("Flash xbee?"):
            self.line("Skipping xbee.")
            return

        if not self._buddyAddress:
            self._buddyAddress = self.ask("Enter the address for the device's buddy: ")

        # https://github.com/python-poetry/cleo/issues/130
        args = f"xbee {self._currentMnFw} {self._buddyAddress} "

        # The default value of None will get passed as the string 'None' if we
        # just include each value
        if self._address:
            args += f"--address {self._address} "
        if self._baudRate:
            args += f"--baudRate {self._baudRate} "
        if self._libFile:
            args += f"--libFile {self._libFile} "
        if self._port:
            args += f"--port {self._port} "
        if self._theme:
            args += f"--theme {self._theme} "

        self.call("xbee", args)

    # -----
    # _flash_microcontroller
    # -----
    def _flash_microcontroller(self, target: str) -> None:
        if target == "habs":
            if not self.confirm("Flash habs?"):
                self.line("Skipping habs.")
                return

        # https://github.com/python-poetry/cleo/issues/130
        args = f"{target} {self._currentMnFw} {self._to} "

        # The default value of None will get passed as the string 'None' if we
        # just include each value
        if self._baudRate:
            args += f"--baudRate {self._baudRate} "
        if self._deviceName:
            args += f"--deviceName {self._deviceName} "
        if self._libFile:
            args += f"--libFile {self._libFile} "
        if self._port:
            args += f"--port {self._port} "
        if self._rigidVersion:
            args += f"--rigidVersion {self._rigidVersion} "
        if self._side:
            args += f"--side {self._side} "
        if self._theme:
            args += f"--theme {self._theme} "

        self.call(target, args)
