from pathlib import Path

from cleo.helpers import argument
from cleo.helpers import option
import semantic_version as sem

from bootloader.utilities.aws import get_remote_file
import bootloader.utilities.config as cfg

from .base_flash_command import BaseFlashCommand


# ============================================
#               FlashMcuCommand
# ============================================
class FlashMcuCommand(BaseFlashCommand):
    """
    Flashing Mn, Ex, Re, and Habs is extremely similar, so this class
    contains the shared functionality that is distinct from flashing bt121
    and xbee.
    """

    arguments = [
        argument("currentMnFw", "Current firmware version on Manage, e.g., `7.2.0`."),
        argument("to", "Desired firmware version, e.g., `9.1.0`, or firmware file."),
    ]
    options = [
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
        option("deviceName", "-d", "Device to flash, e.g., `actpack`.", flag=False),
        option("libFile", "-l", "C lib for interacting with Manage.", flag=False),
        option("port", "-p", "Port the device is on, e.g., `COM3`.", flag=False),
        option("rigidVersion", "-r", "PCB hardware version, e.g., `4.1B`.", flag=False),
        option("side", "-s", "Either left or right.", flag=False),
    ]

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        """
        Sets values of options and arguments to instance attributes.
        """
        self._currentMnFw = self.argument("currentMnFw")
        self._to = self.argument("to")

        self._baudRate = self.option("baudRate")
        self._deviceName = self.option("deviceName")
        self._libFile = self.option("lib")
        self._port = self.option("port")
        self._rigidVersion = self.option("rigidVersion")
        self._side = self.option("side")

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        if sem.validate(self._to):
            fwFile = self._build_fw_file()
        else:
            fwFile = self._to

        self._fwFile = self._handle_file(fwFile)

    # -----
    # _build_fw_file
    # -----
    def _build_fw_file(self) -> str:
        fw = self._to
        devName = self._deviceName if self._deviceName else self._device.deviceName 
        hw = self._rigidVersion if self._rigidVersion else self._device.rigidVersion
        ext = cfg.firmwareExtensions[self._target]

        if self._target == "mn":
            side = f"_side-{self.option('side')}" if self._side else ""

        return f"{devName}_rigid-{hw}_{self._target}_firmware-{fw}{side}.{ext}"

    # -----
    # _handle_file
    # -----
    def _handle_file(self, fwFile: str) -> None:
        fwPath = Path(fwFile).expanduser().absolute()
        if fwPath.exists():
            return fwPath

        fwPath = cfg.firmwareDir.joinpath(fwFile).expanduser().absolute()
        if fwPath.exists():
            return fwPath

        get_remote_file(fwFile, cfg.firmwareBucket, str(fwPath), cfg.dephyProfile)

        return fwPath
