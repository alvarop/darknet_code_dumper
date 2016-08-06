# DC Darknet Code Dumper Tool

## Requirements
* DC Darknet badge (2016)
* ST-Link v2 (JTAG/SWD tool)
* openOCD ([Installation Instructions](http://gnuarmeclipse.github.io/openocd/install/))

## How to use

1. Connect ground on the st-link to ground on the microcontroller
1. Connect SWCLK on the st-link to DCLK on the microcontroller
1. Connect SWDIO on the st-link to DIO on the microcontroller
1. Connect 3.3V on the st-link to 3.3 on the microcontroller
1. Run the following command from this directory:

`python dump_info.py --openocd_dir /opt/gnuarmeclipse/openocd/0.10.0-201601101000-dev/`

![Example connection](stlink.jpg)