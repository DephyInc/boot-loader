from pathlib import Path

from cleo.helpers import argument
from cleo.helpers import option
from flexsea.utilities.aws import s3_download
from flexsea.utilities.firmware import get_closest_version
import semantic_version as sem

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
        option("theme", None, "classic, light, dark, or none", flag=False),
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

        self._baudRate = int(self.option("baudRate"))
        self._deviceName = self.option("deviceName")
        self._libFile = self.option("libFile")
        self._port = self.option("port")
        self._rigidVersion = self.option("rigidVersion")
        self._side = self.option("side")
        self._theme = self.option("theme")

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        # Newer versions of flexsea allow passing "imcomplete" version strings,
        # e.g., '10' or '10.5', both of which are invalid semantic version strings,
        # so we have to try and coerce instead of validating
        try:
            closestFw = get_closest_version(sem.Version.coerce(self._to))
        # This ValueError is raised if the coersion fails, in which case we assume
        # that the value of self._to is the name of the firmware file to flash
        except ValueError:
            fwFile = self._to
        else:
            try:
                # If the given version (self._to) doesn't match what we found on S3
                # then we should make sure closestFw is the version the user wants
                # to flash
                assert closestFw == sem.Version.coerce(self._to)
            except AssertionError:
                if not self.io.is_interactive() and not self.option("no-interaction"):
                    confirmed = input(f"Bootload to: {closestFw} [y/N]?") 
                    if confirmed.lower() != "y":
                        sys.exit(1)
                else:
                    self.line(f"<warning>Flashing to: {closestFw} instead of: {self._to}</warning>")
            self._to = closestFw
            fwFile = self._build_fw_file()
        self._fwFile = self._handle_file(fwFile)

    # -----
    # _build_fw_file
    # -----
    def _build_fw_file(self) -> str:
        devName = self._deviceName if self._deviceName else self._device.deviceName
        hw = self._rigidVersion if self._rigidVersion else self._device.rigidVersion
        ext = cfg.firmwareExtensions[self._target]

        if self._target == "mn":
            side = f"_side-{self._side}" if self._side else ""
        else:
            side = ""

        return f"{devName}_rigid-{hw}_{self._target}_firmware-{self._to}{side}.{ext}"

    # -----
    # _handle_file
    # -----
    def _handle_file(self, fwFile: str) -> None:
        fwPath = Path(fwFile).expanduser().absolute()
        if fwPath.exists():
            return fwPath

        fwPath = cfg.firmwarePath.joinpath(fwFile).expanduser().absolute()
        if fwPath.exists():
            return fwPath

        s3_download(fwFile, cfg.firmwareBucket, str(fwPath), cfg.dephyProfile)

        return fwPath

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        raise NotImplementedError

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        raise NotImplementedError

    # -----
    # _get_target
    # -----
    def _get_target(self) -> None:
        raise NotImplementedError
