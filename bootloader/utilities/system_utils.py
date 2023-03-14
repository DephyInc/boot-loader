from bootloader.utilities import config as cfg


# ============================================
#                setup_cache
# ============================================
def setup_cache() -> None:
    """
    Creates the directories where the firmware files and bootloader
    tools are downloaded and installed to.
    """
    cfg.firmwareDir.mkdir(parents=True, exist_ok=True)
    cfg.toolsDir.mkdir(parents=True, exist_ok=True)
