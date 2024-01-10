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


### Custom Udev Rule

Additional setup in the case that multiple /dev/tty/USB* ports are in use

1. Obtain device information
   - List all connected USB devices along with their Vendor ID and Product ID: ```lsusb```
   - If more detailed info needed: ```sudo lsusb -v```
  
2. Create custom Udev rule
   - ```sudo nano /etc/udev/rules.d/99-usb-serial.rules```
  
3. Add the custom rule
   - Add the following line in the file. Replace `YOUR_VENDOR_ID`, `YOUR_PRODUCT_ID`, `YOUR_SERIAL_NUMBER` with the actual values. If there is no serial number, then omit the `ATTRS{serial}` part
   - ```SUBSYSTEM=="tty", ATTRS{idVendor}=="YOUR_VENDOR_ID", ATTRS{idProduct}=="YOUR_PRODUCT_ID", ATTRS{serial}=="YOUR_SERIAL_NUMBER", SYMLINK+="USB_TO_RS232"```
  
4. Reload Udev rules
   - ```sudo udevadm control --reload-rules && sudo udevadm trigger```
  
5. Verify new setup
   - Disconnect and reconnect the USB-A to RS232 adapter and check if the symlink was created correctly
   - ```ls -l /dev/USB_TO_RS232```
  
6. Update the port in the tester script
   - ```PORT = "/dev/USB_TO_RS232"```
