from cleo.commands.command import Command as BaseCommand


# ============================================
#                 LogoCommand
# ============================================
class LogoCommand(BaseCommand):

    # -----
    # handle
    # -----
    def handle(self) -> int:
        """
        Prints Dephy logo.
        """
        logo = """
        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
        ██░▄▄▀██░▄▄▄██░▄▄░██░██░██░███░██
        ██░██░██░▄▄▄██░▀▀░██░▄▄░██▄▀▀▀▄██
        ██░▀▀░██░▀▀▀██░█████░██░████░████
        ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n\t          Beyond Nature™
        """
        self.line("")
        self.line("")
        try:
            self.line(logo)
        except UnicodeEncodeError:
            self.line("Dephy\nBeyond Nature (TM)")

        return 0
