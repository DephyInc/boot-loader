import glob
import os
import platform
import shutil
import subprocess as sub
import sys
from time import sleep
from typing import List
from typing import Self

from cleo.helpers import argument
from cleo.helpers import option
from flexsea.device import Device

import bootloader.utilities.config as cfg

from .init import InitCommand


# ============================================
#             FlashBt121Command
# ============================================
class FlashBt121Command(InitCommand):
    """
    Flashes the bluetooth 121 radio.
    """

    name = "bt121"

    description = "Flashes the bluetooth radio."

    arguments = [
        argument("firmwareVer", "Current firmware version on Manage, e.g., `7.2.0`."),
    ]

    options = [
        option("address", "-a", "BT address. Default is the device id.", flag=False),
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
        option("level", "-L", "GATT level.", flag=False, default=2),
        option("lib", "-l", "C lib for interacting with current firmware.", flag=False),
        option("port", "-p", "Port the device is on, e.g., `COM3`.", flag=False),
    ]

    help = """
    Creates a new bluetooth file with the desired GATT level and flashes it
    onto the device's bt121 radio.

    `--level` is the level of the gatt file to use. Default is 2.

    `--address` is the desired bluetooth address. If not specificed, the device ID
    is used.

    Examples
    --------
    bootload bt121 7.2.0
    bootload bt121 9.1.0 --level 2 --address 0001
    """

    _address: str = ""
    _device: None | Device = None
    _flashCmd: List[str] = []
    _fwFile: str = ""
    _level: int | None = None
    _nRetries: int = 5
    _port: str = ""
    _target: str = "bt"

    # -----
    # handle
    # -----
    def handle(self: Self) -> int:
        self._stylize()
        self._configure_interaction()
        self._configure_unicode()
        self._setup_environment()
        self._get_device()
        self._build_bt_image()
        self._set_tunnel_mode()
        self._flash()

        return 0

    # -----
    # _get_device
    # -----
    def _get_device(self: Self) -> None:
        self._device = Device(
            self.option("port"),
            int(self.option("baudRate")),
            self.argument("firmwareVer"),
            libFile=self.option("lib"),
        )
        self._port = self._device.port
        self._device.open()

    # -----
    # _build_bt_image
    # -----
    def _build_bt_image(self) -> None:
        """
        Uses the bluetooth tools repo (downloaded as a part of `init`)
        to create a bluetooth image file with the correct address.
        """
        self.write("Building bluetooth image...")

        self._level = self.option("level")
        if self.option("address"):
            self._address = self.option("address")
        else:
            self._address = self._device.deviceId

        # Everything within the bt121 directory is self-contained and
        # self-referencing, so it's easiest to switch to that directory
        # first
        cwd = os.getcwd()
        # The way the zip is decompressed creates this nested structure
        os.chdir(os.path.join(cfg.toolsDir, "bt121_image_tools", "bt121_image_tools"))

        gattTemplate = os.path.join("gatt_files", f"LVL{self._level}.xml")
        gattFile = os.path.join("dephy_gatt_broadcast_bt121", "gatt.xml")

        if not os.path.exists(gattTemplate):
            raise FileNotFoundError(f"Could not find: `{gattTemplate}`.")

        shutil.copyfile(gattTemplate, gattFile)

        if "linux" in platform.system().lower():
            pythonCommand = "python3"
        elif "windows" in platform.system().lower():
            pythonCommand = "python"
        else:
            raise OSError("Unsupported OS!")

        cmd = [pythonCommand, "bt121_gatt_broadcast_img.py", f"{self._address}"]
        proc = sub.run(cmd, capture_output=False, check=True, timeout=360)

        if proc.returncode != 0:
            raise RuntimeError("bt121_gatt_broadcast_img.py failed.")

        bgExe = os.path.join("smart-ready-1.7.0-217", "bin", "bgbuild.exe")
        xmlFile = os.path.join("dephy_gatt_broadcast_bt121", "project.xml")
        proc = sub.run([bgExe, xmlFile], capture_output=False, check=True, timeout=360)

        if proc.returncode != 0:
            raise RuntimeError("bgbuild.exe failed.")

        if os.path.exists("output"):
            files = glob.glob(os.path.join("output", "*.bin"))
            for file in files:
                os.remove(file)
        else:
            os.mkdir("output")

        btImageFile = f"dephy_gatt_broadcast_bt121_Exo-{self._address}.bin"
        shutil.move(os.path.join("dephy_gatt_broadcast_bt121", btImageFile), "output")
        btImageFile = os.path.join(os.getcwd(), "output", btImageFile)

        os.chdir(cwd)

        self._fwFile = btImageFile
        self.overwrite(f"Building bluetooth image... {self._SUCCESS}\n")

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
    def _flash(self) -> None:
        self.write(f"Flashing {self._target}...")

        self._device.close()

        sleep(3)
        self._call_flash_tool()
        sleep(20)

        if not self.confirm("Please power cycle device.", False):
            sys.exit(1)
        self.overwrite(f"Flashing {self._target}... <success>✓</success>\n")

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
        cmd = [
            os.path.join(cfg.toolsDir, "stm32flash"),
            "-w",
            f"{self._fwFile}",
            "-b",
            "115200",
            self._device.port,
        ]

        return cmd
