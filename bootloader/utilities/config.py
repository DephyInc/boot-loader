from pathlib import Path


# ============================================
#              Path Configuration
# ============================================

# Root directory of where to save bootloading tools and downloaded
# firmware
cacheDir = Path.joinpath(Path.home(), ".dephy", "bootloader")

# Directory to save bootloading tools
toolsDir = cacheDir.joinpath("tools")

# Directory to save firmware
firmwareDir = cacheDir.joinpath("firmware")


# ============================================
#              S3 Configuration
# ============================================

# Public bucket where bootloading tools are stored
toolsBucket = "dephy-bootloader-tools"

# Private bucket where the firmware is stored
firmwareBucket = "dephy-firmware"

# Public bucket where the pre-compiled C libraries are stored
libsBucket = "dephy-public-binaries"

# Credentials profile name
dephyProfile = "dephy"

# Dummy file to check AWS key authenticity
connectionFile = "connection_file.txt"

# AWS credentials file
credentialsFile = Path.joinpath(Path.home(), ".aws", "credentials")


# ============================================
#                Dependencies
# ============================================
bootloaderTools = {
    "windows": {
        "bt121" : ["bt121_image_tools.zip", "stm32flash.exe",],
        "ex" : ["psocbootloaderhost.exe",],
        "habs" : ["stm32_flash_loader.zip",],
        "mn" : ["DfuSeCommand.exe",],
        "re" : ["psocbootloaderhost.exe",],
        "xbee" : ["XB24C.zip",],
    },
}


# ============================================
#                 Constants
# ============================================
baudRate = 230400
firmwareExtensions = {"habs": "hex", "ex": "cyacd", "re": "cyacd", "mn": "dfu"}
targets = ["habs", "ex", "re", "bt121", "xbee", "mn"]
supportedOS = [
    "windows",
]


# ============================================
#                   Themes
# ============================================
themes = {
    "classic": {
        "info": {"fg": "blue", "options": []},
        "warning": {"fg": "yellow", "options": []},
        "error": {
            "fg": "red",
            "options": [
                "bold",
            ],
        },
        "success": {
            "fg": "green",
            "options": [
                "bold",
            ],
        },
    },
    "light": {
        "info": {"fg": "light_blue", "options": []},
        "warning": {"fg": "light_yellow", "options": []},
        "error": {
            "fg": "light_red",
            "options": [
                "bold",
            ],
        },
        "success": {
            "fg": "light_green",
            "options": [
                "bold",
            ],
        },
    },
    "dark": {
        "info": {
            "fg": "blue",
            "options": [
                "dark",
            ],
        },
        "warning": {
            "fg": "yellow",
            "options": [
                "dark",
            ],
        },
        "error": {
            "fg": "red",
            "options": [
                "dark",
                "bold",
            ],
        },
        "success": {
            "fg": "green",
            "options": [
                "dark",
                "bold",
            ],
        },
    },
    "none": {
        "info": {"fg": "default", "options": []},
        "warning": {"fg": "default", "options": []},
        "error": {"fg": "default", "options": []},
        "success": {"fg": "default", "options": []},
    },
}
