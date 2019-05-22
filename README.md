# BOSCH GLM rangefinder

Python3 script to remote control a BOSCH GLM 100C or GLM 50C rangefinder.

This script provides remote control features for the BOSCH GLM 100C/50C measuring device via its Bluetooth serial interface. The device uses the transfer protocol as described [in this blog post](https://www.eevblog.com/forum/projects/hacking-the-bosch-glm-20-laser-measuring-tape/msg1331649/#msg1331649).

As the protocol seems to be identical for various Bosch measuring devices this script could also work for Bluetooth enabled rangefinders like PLR30C, PLR40C or PLR50C. If so please let me know!

## Features

* measure (returns distance millimeters)
* turn laser on and off
* turn display backlight on and off

## Dependencies

The script was only tested on Windows. But since the Python module used is multi-platform, it should also support Linux and MacOS. See [pybluez](https://github.com/pybluez/pybluez) for further information.


Install `pybluez` for the Python3 interpreter via `pip`:

```bash
pip3 install pybluez
```

## Run the script

### Use the command line tool

```bash
python3 glm100c.py
```

Instructions on how to use get printed to the command line.

### Import into your project

```python
from glm100c import GLM100C

rangefinder = GLM100C()
if not rangefinder.connected: exit(1) 

distance = rangefinder.measure_from_tripod_socket()
if distance is not -1: print(distance, 'mm')
```
