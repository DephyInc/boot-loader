# ============================================
#               FlashAllCommand
# ============================================
class FlashAllCommand(FlashMcuCommand):
    """
    Flashes known-good firmware for Habs, Ex, Re, bt121, xbee, and Mn.
    """

    name = "all"

    description = "Flashes known-good firmware for Habs, Ex, Re, bt121, xbee, and Mn."

    help = """
    Flashes known-good firmware for Habs, Ex, Re, bt121, xbee, and Mn. This means
    that the `to` argument must be a semantic version string for a version on S3.
    Since xbee is also being flashed, we require the bluetooth address of the
    current device's buddy as the third argument.

    Examples
    --------
    # Flash from version 7.2.0 to version 9.1.0 and pair xbee with address 1234
    > bootload all 7.2.0 9.1.0 1234
    """

    # -----
    # __new__
    # -----
    def __new__(cls):
        obj = super().__new__(cls)
        obj.arguments.append(argument("buddyAddress", "BT address of device's buddy."))
        return obj

    # -----
    # handle
    # -----
    def handle(self) -> int:
        self._setup()
        self._ensure_interaction()

        for cmd in ["bt121", "xbee", "habs", "ex", "re", "mn"]:
            params = self._build_param_list(cmd)
            self.call(cmd, *params)

        return 0

    # -----
    # _ensure_interaction
    # -----
    def _ensure_interaction(self) -> None:
        """
        The device needs to be power-cycled after each MCU is flashed,
        so we require that interaction be on in order to wait for the
        user to power-cycle.
        """
        if self.option("quiet"):
            raise RuntimeError("Cannot flash all with `--quiet` set.")
        self.io.interactive(True)

    # -----
    # _build_param_list
    # -----
    def _build_param_list(self, target):
        args = self._build_arg_list(target)
        opts = self._build_opt_list()

        return args + opts

    # -----
    # _build_arg_list
    # -----
    def _build_arg_list(self, target):
        args = [self.argument("mnFirmware"),]
        if target == "xbee":
            args.append(self.argument("buddyAddress"))
        elif target in ("habs", "ex", "re", "mn"):
            args.append(self.argument("to"))
        return args

    # -----
    # _build_opt_list
    # -----
    def _build_opt_list(self):
        options = []
        for opt in self.options:
            if opt.is_flag() and self.option(f"{opt.name}"):
                options.append(f"--{opt.name}")
            if opt.requires_value() and self.option(f"{opt.name}") is not None:
                options.append(f"--{opt.name} {self.option(f'{opt.name'})}")
        return options
