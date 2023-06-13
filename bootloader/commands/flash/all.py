# ============================================
#               FlashAllCommand
# ============================================
class FlashAllCommand(BaseCommand):
    """
    Flashes bt121, xbee, habs, ex, re, and then mn.
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.name = "flash all"
        self.description = "Flashes new firmware onto bt121, xbee, habs, ex, re, and mn"
        self.help = self._help()

        self.options.append(
            option("address", "-a", "Bluetooth address. Default is the device id.", flag=False),
            option("buddyAddress", None, "Bluetooth address of device's buddy.", flag=False),
            option("device", "-d", "Device to flash, e.g., `actpack`.", flag=False),
            option("side", "-s", "Either left or right.", flag=False),
            option("rigidVersion", "-r", "PCB hardware version, e.g., `4.1B`.", flag=False),
            option("motorType", "-r", "Either 'actpack', 'exo', or '6:1-9:1'.", flag=False),
            option("i2t", "-r", "i2t preset letter. Default is B before 10 and D after..", flag=False),
            option("led", "-r", "Either 'mono', 'multi', or 'stealth'.", flag=False),
            option("desired-mn-version", None, "Version or file to use when flashing Mn", flag=False),
            option("desired-ex-version", None, "Version or file to use when flashing Ex", flag=False),
            option("desired-re-version", None, "Version or file to use when flashing Re", flag=False),
            option("desired-habs-version", None, "Version or file to use when flashing Habs", flag=False),
        ]

        self._currentMnFw: str = ""
        self._to: str = ""
        self._address: str = ""
        self._baudRate: int | None = None
        self._buddyAddress: str = ""
        self._deviceName: str = ""
        self._level: int | None = None
        self._libFile: str = ""
        self._port: str = ""
        self._rigidVersion: str = ""
        self._side: str = ""

        self.hidden = False
