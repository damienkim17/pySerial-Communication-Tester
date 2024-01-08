# pySerial-Communication-Tester
Python script to test serial configurations on a device connected to rasbpi4

### Setup:

1. Install pySerial
   - ```sudo pip3 install pyserial```

2. Transfer the script to the Raspberry Pi
   - ```scp scp "path\to\your\script.py" pi@Pi_IP_Address:/home/pi/.serial_tester```
  
3. Make the script executable
   - ```chmod +x serial_tester.py```


### Verify connected device:

Assumes that the pi4 is connected to the device via USB-A to RS232, using the /dev/ttyUSB0 port

  Check USB devices: Shows the adapter's vendor and product IDs
    - ```lsusb```

  Check dmesg: Shows the kernel messages
    - ```dmesg | grep ttyUSB```

  Check device file: Ensure that /dev/ttyUSB0 exists after you connect the adapter. If it's the only serial device, it should be /dev/ttyUSB0
    - ```ls /dev/ttyUSB*```

  
