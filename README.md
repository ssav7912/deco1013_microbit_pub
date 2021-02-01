# deco1013-microbit

unikey: ssav7912

Name: Soren Saville Scott

## Description
This repository contains python code and firmware for my DECO1013 proposal. ProposalMerge.py contains main running code that controls a wireless lamp system with controls for Hue and saturation, that transmits its state to its partner periodically. 

## Hardware Requirements
Requires 2 of:
- BBC Micro:bit
- (Optional but recommended - Grove Micro:bit shield)
- Grove I2C Touch Feelers MPR121 https://wiki.seeedstudio.com/Grove-I2C_Touch_Sensor/ (4 feelers mapped to 0-3)
- Adafruit WS2182 5050 16x RGBW neopixel ring on pin0. 

## Dependencies
1. Custom micropython runtime for RGBW neopixel support. Can be found at `firmware.hex` in the `/build` directory, or built from source here: https://github.com/ssav7912/micropython/tree/RGBW-Support
2. Requires the `makecombinedhex.py` script (and dependencies) from the micropython micro:bit source repository. Can be found in the `tools` directory of the repository above.
3. Requires a python minifier to compress the script and fit onto the micro:bit memory. `pyminifier` is recommended: https://github.com/liftoff/pyminifier

## Installation
For a direct, easy install, one can flash the `main.hex` runtime file in the `/build` directory directly to your micro:bit's with uflash, Mu, or whatever you prefer.

However, if you would like to modify this source:

### Building
This script requires a custom micropython runtime in order to be compatible with the RGBW Neopixel ring. A copy of this firmware has been included in the `build` directory, named `firmware.hex`.

I recommend making a copy of your changes to operate on first.
1. Minify your script using your minifier, e.g. `pyminify`:
```bash
$: pyminify ProposalMergeBackup.py > ProposalMini.py
```
2. Compile this minified script into your firmware hex file, e.g. like so:
```bash
$: python3 makecombinedhex.py -o main.hex build/firmware.hex ProposalMini.py
```
3. Upload your combined hex file to your micro:bits, either with uflash or Mu. e.g:
```bash
$: uflash --runtime=main.hex
```
If you are going to make repeated changes, i.e. for testing, I recommend deleting your minified script and your combined hex file before making them again, as I seemed to have issues if they were kept around and overwritten.
