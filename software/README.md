# Software Guide

## Installation Instructions

The Installation consists of two parts: the Feather M4 and the Arduino Nano.

### Feather M4

1. OPTIONAL BUT RECOMMENDED: Update the Bootloader on the Feather M4 to the latest version (the one preinstalled might be quite old which can cause issues with CircuitPython 5.x).
    1. Download the latest firmware updater from [its home](https://github.com/adafruit/uf2-samdx1/releases). Look for a download with a file name of this pattern: `update-bootloader-feather_m4-vx.x.x.uf2`.
    2. Plug the Feather M4 into a USB port on your computer.
    3. Double click the board's reset button. Once the bootloader is active you will see the small red LED fade in and out and a drive named `FEATHERBOOT` should appear.
    4. And copy the updater to the drive presented by the Feather M4 (`FEATHERBOOT`).
    5. Wait a few seconds until the Neopixel turns green and `FEATHERBOOT` reappears, and proceed!
2. Download and install CircuitPython.
    1. Download an appropriate version of CircuitPython from the [board's homepage on circuitpython.org](https://circuitpython.org/board/feather_m4_express/). NOTE: any version should work, but this was developed and tested with CircuitPython 5.2.0.
    2. Plug the Feather M4 into a USB port on your computer.
    3. Double click the board's reset button. Once the bootloader is active you will see the small red LED fade in and out and a drive named `FEATHERBOOT` should appear.
    4. And copy CircuitPython to the drive presented by the Feather M4 (`FEATHERBOOT`).
3. Download and install the required libraries.
    1. Download the latest library version matching your CircuitPython version from [here](https://circuitpython.org/libraries).
    2. Unzip the zip file.
    3. Create a folder on the board's drive (now named `CIRCUITPY`) named `lib`.
    4. Copy these libraries into that folder:
        1. adafruit_ads1x15
        2. adafruit_bmp3xx
        3. adafruit_ccs811
        4. adafruit_gps
        5. adafruit_pcf8523
        6. adafruit_sdcard
        7. adafruit_sht31d
        8. neopixel
4. Copy the program to the board.
    1. Download a copy of `on-drone.py` from the same folder as this document.
    2. Rename it to `code.py`.
    3. Copy it to the root of `CIRCUITPY`.
5. Enjoy!

### Arduino Nano

1. [Download](https://www.arduino.cc/en/Main/Software#download) and install the Arduino IDE onto your computer.
2. Open the `pms5003.ino` sketch in the Arduino IDE.
3. Select the correct serial port in the `Tools > Port` menu.
    1. On macOS, this often begins with `/dev/tty.usbserial`, `/dev/tty.wchusbserial`, or `/dev/tty.SLAB_USB`.
    2. On Windows, this will be a `COM` port.
    3. On Linux, this should begin with `/dev/ttyUSB`.
4. Upload the sketch to the board by clicking the Upload button.
