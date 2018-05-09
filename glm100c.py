#!/usr/bin/env python

"""
Connect and control a BOSCH GLM100C laser range finder via Bluetooth
May be adaptable for similar Bluetooth enabled BOSCH measuring devices, like GLM50C, PLR30C, PLR40C or PLR50C

Author: Philipp Trenz
"""

import bluetooth # install pybluez
import struct

class GLM100C(object):
    """
    Bluethooth Connection to laser range finder GLM100C
    """
    socket = None
    port = 0x0001
    bluetooth_address = None
    connected = False

    # See: https://www.eevblog.com/forum/projects/hacking-the-bosch-glm-20-laser-measuring-tape/msg1331649/#msg1331649
    #
    #   send frame:    [startbyte][command][length]([data])[checksum]
    #   receive frame: [status][length][...][checksum]

    cmds = {
        'measure':          b'\xC0\x40\x00\xEE',
        'laser_on':         b'\xC0\x41\x00\x96',
        'laser_off':        b'\xC0\x42\x00\x1E',
        'backlight_on':     b'\xC0\x47\x00\x20',
        'backlight_off':    b'\xC0\x48\x00\x62'
    }

    status = {
        0:  'ok',
        1:  'communication timeout',
        3:  'checksum error',
        4:  'unknown command',
        5:  'invalid access level',
        8:  'hardware error',
        10: 'device not ready',
    }

    def __init__(self, bluetooth_address=None):
        if bluetooth_address is None:
            self.find_GLM100C()
        else:
            self.bluetooth_address = bluetooth_address
        self.connect()


    def connect(self):
        try:
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((self.bluetooth_address, self.port))
            self.connected = True
            #print('BOSCH GLM100C connected')
        except:
            self.socket.close()
            self.conencted = False
            #print('Connecting to BOSCH GLM100C failed')

    def find_GLM100C(self):
        print('Searching for BOSCH GLM100C ...')

        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

        for index, val in enumerate(nearby_devices):
            addr, name = val
            if 'BOSCH GLM100C' in name.upper():
                self.bluetooth_address = addr
                print('Found BOSCH GLM100C @', self.bluetooth_address)
                return

    def measure(self):
        self.socket.send(self.cmds['measure'])
        data = self.socket.recv(1024)
        #print('received:', data)

        if self.status[data[0]] is 'ok':
            try:
                # distance to object from top of device
                distance = int(struct.unpack("<L", data[2:6])[0])*0.05
                #print(distance, 'mm')
                return distance
            except:
                #print('corrupt data received, try again')
                return -1
        else:
            return -1

    def measure_from_top(self):
        return self.measure()

    def measure_from_tripod_socket(self):
        m = self.measure()
        if m is -1: return m
        return m+40

    def measure_from_back(self):
        m = self.measure()
        if m is -1: return m
        return m+110

    def turn_laser_on(self):
        self.socket.send(self.cmds['laser_on'])
        self.socket.recv(1024)

    def turn_laser_off(self):
        self.socket.send(self.cmds['laser_off'])
        self.socket.recv(1024)

    def turn_backlight_on(self):
        self.socket.send(self.cmds['backlight_on'])
        self.socket.recv(1024)

    def turn_backlight_off(self):
        self.socket.send(self.cmds['backlight_off'])
        self.socket.recv(1024)

    def raw_command(self, cmd):
        if isinstance(cmd, bytes):
            #print('sending:\t', cmd)
            self.socket.send(cmd)
            data = self.socket.recv(1024)
            #print('received:\t', data)

            status = self.status[data[0]]
            #print(self.status[data[0]])

            return (data, status)
        else:
            print('no bytes, ignoring')
            return None

    def find_bluetooth_services(self):
        services = bluetooth.find_service(address=self.bluetooth_address)
        if len(services) > 0:
            print("found %d services on %s" % (len(services), self.bluetooth_address))
            print(services)
        else:
            print("no services found")

    def close(self):
        self.socket.close()




if __name__ == "__main__":

    rangefinder = GLM100C()

    # connecting can be speeded up when the mac address of the device is known, e.g.:
    # rangefinder = GLM100C(bluetooth_address='54:6C:0E:29:92:2F') 


    # print('')
    # rangefinder.find_bluetooth_services()
    # print('')

    if rangefinder.connected:
        print('Connected BOSCH GLM100C @', rangefinder.bluetooth_address)

        try:
            print('\ntype \'m\' to measure, \n\'lon\' or \'loff\' to turn laser on/off, \n\'bon\' or \'boff\' to turn backlight on/off,\n\'x\' to exit\n')

            while True:
                data = input()
                if data == 'm':
                    distance = rangefinder.measure()
                    if distance > 0:
                        print(distance, 'mm from top of device')
                        print(distance+40.0, 'mm from tripod socket')
                        print(distance+110.0, 'mm from back of device')
                elif data == 'lon':
                    rangefinder.turn_laser_on()
                elif data == 'loff':
                    rangefinder.turn_laser_off()
                elif data == 'bon':
                    rangefinder.turn_backlight_on()
                elif data == 'boff':
                    rangefinder.turn_backlight_off()
                elif data == 'x':
                    rangefinder.close()
                    print('Connection to BOSCH GLM100C closed')
                    break

        except KeyboardInterrupt:
            rangefinder.close()
            print('Connection to BOSCH GLM100C closed')
    else:
        print('Could not connect to BOSCH GLM100C')
