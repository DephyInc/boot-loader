# ============================================
#                  AllCommand
# ============================================
class AllCommand:
    """
    Flashes Habs, Ex, Re, Mn, Bt121, and Xbee to known-good firmware.
    """
    name = "all"

    description = "Flashes Habs, Ex, Re, Mn, Bt121, and Xbee to known-good firmware."

    arguments = [
        argument("from", "Current firmware version on Manage, e.g., `7.2.0`."),
        argument("to", "Desired firmware version, e.g., `9.1.0`."),
    ]

    options = [
        option("lib", "-l", "C lib for interacting with current firmware.", flag=False),
        option("port", "-p", "Port the device is on, e.g., `COM3`.", flag=False),
        option("hardware", "-r", "Board hardware version, e.g., `4.1B`.", flag=False),
        option("device", "-d", "Device to flash, e.g., `actpack`.", flag=False),
        option("side", "-s", "Either left or right.", flag=False),
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
    ]

    help = ""

    # -----
    # handle
    # -----
    def handle(self) -> int:
        mcuArgs = self._get_mcu_args()
        mcuOpts = self._get_mcu_opts()
        radioArgs = self._get_radio_args()
        radioOpts = self._get_radio_opts()

        for target in cfg.targets:
            if target in cfg.microcontrollers:
                self.call("micro", f"{target} {mcuArgs}", mcuOpts)
            elif target in cfg.radios:
