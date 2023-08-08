# Dephy Bootloader

This is a command-line tool for flashing firmware onto Dephy's wearable robotic devices.


## Installation
See the guide [here](./docs/install.md).


## Usage

**TL;DR** The *list* command is your friend (`bootloader list`).
For more, see the documentation [here](./docs/api.md).


## INTERNAL NOTES

If you need to find the correct stusb.sys driver: 

C: / Program Files (x86) > STMicroelectronics > Software > DfuSE v3.0.6 > Driver > Win 10
Driver folder might be under Bin


For purging bootloader drivers (installed with the cube link):

https://www.winhelponline.com/blog/driver-uninstall-completely-windows/
dism /online /get-drivers /format:table 
pnputil /delete-driver <Published Name> /uninstall /force


There's some dll needed by DfUSE. I had it because I had previously installed it and 
added the directory to my path. Users will not necesarily have done that, so we just 
download the whole thing and locally export PATH to have this dir:

*https://drive.google.com/file/d/10n0WdbGc9thBqayA13df-fIe_pN1Te3D/view?usp=sharing (dfuse setup for mn) (need whole Dfuse directory)

* Remove link to stm32 cube for drivers. Use st link utility drivers


USE THIS FOR DRIVERS: https://drive.google.com/drive/folders/1wGDykIJSNwJn5nOcrUDw1VMRk9d_GOmx?usp=drive_link
The actual name of the driver is something like ST Device in DfUSE Mode


We need a VERY specific version of mingw for psocbootloaderhost to work.

This is the zip: https://drive.google.com/file/d/1G5SRalr-VXXg49JD8wQofabTC5Qcbnd8/view?usp=drive_link

This is the installer: https://drive.google.com/file/d/1mOU070KCyBvSVbgFDS_N9Fm79fuypA5R/view?usp=drive_link

Not sure what the difference between the above two are. I only need one, but not sure which
