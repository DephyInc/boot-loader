import os
import platform
import subprocess as sub
import sys
from time import sleep

from cleo.helpers import argument
from cleo.helpers import option
from flexsea.device import Device

from .init import InitCommand


# ============================================
#            FlashXbeeCommand
# ============================================
class FlashXbeeCommand(InitCommand):
    """
    Sets up the xbee radio for inter-device communication.
    """

    name = "xbee"
    
    description = "Sets up the xbee radio for inter-device communication."

    arguments = [
        argument("firmwareVer", "Current firmware version on Manage, e.g., `7.2.0`."),
        argument("buddyAddress", "Address of device's buddy."),
    ]

    options = [
        option("address", "-a", "BT address. Default is the device id.", flag=False),
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
        option("lib", "-l", "C lib for interacting with current firmware.", flag=False),
        option("port", "-p", "Port the device is on, e.g., `COM3`.", flag=False),
    ]

    help = ""

    _address: str = ""
    _device: None | Device = None
    _nRetries: int = 5
    _port: str = ""
    _target: str = "xbee"

    # -----
    # handle
    # -----
    def handle(self) -> int:
        self._stylize()
        self._configure_interaction()
        self._configure_unicode()
        self._setup_environment()
        self._get_device()

        if self.option("address"):
            self._address = self.option("address")
        else:
            self._address = self._device.devId

        self._set_tunnel_mode()
        self._flash()

        return 0

    # -----
    # _get_device
    # -----
    def _get_device(self) -> None:
        self._device = Device(
            self.option("port"),
            int(self.option("baudRate")),
            self.argument("mnFirmware"),
            libFile=self.option("lib"),
        )
        self._port = self._device.port
        self._device.open()

    # -----
    # _set_tunnel_mode
    # -----
    def _set_tunnel_mode(self) -> None:
        msg = "<warning>Please make sure the battery is removed "
        msg += "and/or the power supply is disconnected!</warning>"
        if not self.confirm(msg, False):
            sys.exit(1)
        self.write(f"Setting tunnel mode for {self._target}...")

        if not self._device.set_tunnel_mode(self._target, 20):
            msg = "\n<error>Error</error>: failed to activate bootloader for: "
            msg += f"<info>`{self._target}`</info>"
            self.line(msg)
            sys.exit(1)

        self.overwrite(f"Setting tunnel mode for {self._target}... {self._SUCCESS}\n")

    # -----
    # _flash
    # -----
    def _flash(self: Self) -> None:
        self.write(f"Flashing {self._target}...")

        self._device.close()

        sleep(3)
        self._call_flash_tool()
        sleep(20)

        if not self.confirm("Please power cycle device.", False):
            sys.exit(1)
        self.overwrite(f"Flashing {self._target}... {self._SUCCESS}\n")

    # -----
    # _call_flash_tool
    # -----
    def _call_flash_tool(self) -> None:
        for _ in range(self._nRetries):
            try:
                proc = sub.run(
                    self._flashCmd, capture_output=False, check=True, timeout=360
                )
            except sub.CalledProcessError:
                continue
            except sub.TimeoutExpired:
                self.line("Timeout.")
                sys.exit(1)
            if proc.returncode == 0:
                break
        if proc.returncode != 0:
            self.line("Error.")
            sys.exit(1)

    # -----
    # _flashCmd
    # -----
    @property
    def _flashCmd(self) -> List[str]:
        _os = platform.system().lower()

        if _os == "windows":
            pythonCmd = "python"
        else:
            pythonCmd = "python3"

        cmd = [
            pythonCmd,
            os.path.join(cfg.toolsDir, "xb24c.py"),
            self._port,
            self._address,
            self.argument("buddyAddress"),
            "upgrade",
        ]
        return cmd
