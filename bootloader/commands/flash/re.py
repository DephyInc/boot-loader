from cleo.helpers import argument
from flexsea.utilities.firmware import validate_given_firmware_version


from bootloader.commands.flash.mcu import FlashMcuCommand


# ============================================
#              FlashReCommand
# ============================================
class FlashReCommand(FlashMcuCommand):

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash re"
        self.description = "Flashes new firmware onto Regulate."
        self.help = self._help()
        self.hidden = False

        self.arguments.append(
            argument("led", "Either 'mono', 'multi', or 'stealth'")
        )

        self._led: str = ""

    # -----
    # _parse_options
    # -----
    def _parse_options(self) -> None:
        super()._parse_options()
        self._led = self.argument("led")
        self._target = "re"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, desiredFirmwareVersion: Version) -> None:
        fName = f"{self._target}_version-{desiredFirmwareVersion}_"
        fName += f"rigid-{self._rigidVersion}_led-{self._led}color.cyacd"

        self._fwFile = fxc.dephyPath.joinpath(bc.firmwareDir, fName)

        if not fwFile.is_file():
            s3_download(fName, bc.dephyFirmwareBucket, self._fwFile, bc.dephyAwsProfile)

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            f"{Path.joinpath(cfg.toolsPath, 'psocbootloaderhost.exe')}",
            f"{self._port}",
            f"{self._fwFile}",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        sleep(3)
        self._device.close()
        call_flash_tool(self._flashCmd)

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line("<info>Summary</>:")
        self.line(f"\t* LED pattern being used: {self._led}")
        super()._confirm()

    # -----
    # _help
    # -----
    def _help(self) -> str:
        return "Flashes new firmware onto Regulate."
