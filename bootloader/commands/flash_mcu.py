from pathlib import Path
import subprocess as sub
import sys
from typing import List

from cleo.helpers import argument
from cleo.helpers import option
from flexsea.device import Device
import semantic_version as sem

import bootloader.utilities.config as cfg
from bootloader.utilities.aws import get_flash_tools
from bootloader.utilities.aws import get_remote_file

from .base_command import BaseCommand


# ============================================
#             FlashMcuCommand
# ============================================
class FlashMcuCommand(BaseCommand):

    arguments = [
        argument("mnFirmware", "Current firmware version on Manage, e.g., `7.2.0`."),
        argument("to", "Desired firmware version, e.g., `9.1.0`, or firmware file."),
    ]

    _device: None | Device = None
    _fwFile: str = ""
    _target: str = ""

    # -----
    # __new__
    # -----
    def __new__(cls):
        obj = super().__new__(cls)

        obj.options.append(
            option("baudRate", "-b", "Device baud rate.", flag=False, default=230400)
        )
        obj.options.append(
            option("deviceName", "-d", "Device to flash, e.g., `actpack`.", flag=False)
        )
        obj.options.append(
            option(
                "hardware", "-r", "Board hardware version, e.g., `4.1B`.", flag=False
            )
        )
        obj.options.append(
            option(
                "lib", "-l", "C lib for interacting with current firmware.", flag=False
            )
        )
        obj.options.append(
            option("port", "-p", "Port the device is on, e.g., `COM3`.", flag=False)
        )
        obj.options.append(option("side", "-s", "Left or right.", flag=False))

        return obj

    # -----
    # handle
    # -----
    def handle(self) -> int:
        self._setup()
        self._get_device()
        self._get_firmware_file()
        get_flash_tools(self._target, self._os)
        self._set_tunnel_mode()
        self._flash()

        return 0

    # -----
    # _get_device
    # -----
    def _get_device(self) -> None:
        self._device = Device(
            port=self.option("port"),
            baudRate=int(self.option("baudRate")),
            cLibVersion=self.argument("mnFirmware"),
            libFile=self.option("lib"),
        )
        self._device.open()

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        if sem.validate(self.argument("to")):
            fwFile = self._build_fw_file()
        else:
            fwFile = self.argument("to")

        self._fwFile = self._handle_file(fwFile)

    # -----
    # _build_fw_file
    # -----
    def _build_fw_file(self) -> str:
        devName = self.option("deviceName")
        hw = self.option("hardware")

        devName = devName if devName else self._device.deviceName
        hw = hw if hw else self._device.rigidVersion
        fw = self.argument("to")
        ext = cfg.firmwareExtensions[self._target]

        if self._target == "mn":
            side = f"_side-{self.option('side')}" if self.option("side") else ""
        else:
            side = ""

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

        get_remote_file(fwFile, cfg.firmwareBucket, str(fwPath))

        return fwPath

    # -----
    # _set_tunnel_mode
    # -----
    def _set_tunnel_mode(self) -> None:
        msg = "<warning>Please make sure the battery is removed "
        msg += "and/or the power supply is disconnected!</warning>"

        if not (self.option("no-interaction") or self.option("quiet")):
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
    # _call_flash_tool
    # -----
    def _call_flash_tool(self) -> None:
        for _ in range(5):
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
    # _flash
    # -----
    def _flash(self) -> None:
        self.write(f"Flashing {self._target}...")
        self._flash_target()
        if not self.confirm("Please power cycle device.", False):
            sys.exit(1)
        self.overwrite(f"Flashing {self._target}... {self._SUCCESS}\n")

    # -----
    # _flashCmd
    # -----
    @property
    def _flashCmd(self) -> List[str]:
        raise NotImplementedError

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        raise NotImplementedError
