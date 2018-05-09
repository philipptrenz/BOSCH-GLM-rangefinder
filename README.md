# BOSCH GLM rangefinder

Python3 script to remote control a BOSCH GLM 100C rangefinder.

This script provides remote control features for the BOSCH GLM 100C measuring device via its Bluetooth serial interface. The device uses the same transfer protocol as described [in this blog post](https://www.eevblog.com/forum/projects/hacking-the-bosch-glm-20-laser-measuring-tape/msg1331649/#msg1331649).

## Features

* measure, returns a distance in millimeters
* turn laser on and off
* turn display backlight on and off

## Dependencies

The script was only tested on Windows. But since the Python module used is multi-platform, it should also support MacOS, Linux and the ARM system of the Raspberry Pi. See [pybluez](https://github.com/pybluez/pybluez) for further information.


Install `pybluez` for the Python3 interpreter via `pip`:

```
pip3 install pybluez
```

## Run the script

```
python3 glm100c.py
```