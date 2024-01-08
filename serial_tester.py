import serial
import time

# Define the base barcode data here as a byte string
BASE_BARCODE_DATA = b'123456789012'  # Replace with your valid barcode data

# Define possible endings for the barcode: carriage return, newline, or none
# CR common for POS to signify end of data entry, mimicing the enter key on a kb
# NL used for multi-line input or by unix systems
# CRNL common in windows-based systems as a standard end-of-line marker
BARCODE_ENDINGS = [b'\r', b'\n', b'\r\n']  # CR, NL, CRNL

# Common baud rates
BAUDRATES = [9600, 115200, 19200, 38400, 57600, 230400, 460800, 921600]

# Standard parity options - Excluding Mark and Space
PARITIES = [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD]

# Data bits - Focusing on 7 and 8
DATABITS = [8, 7]

# Stop bits - Unchanged as only two options were there initially
STOPBITS = [serial.STOPBITS_ONE, serial.STOPBITS_TWO]

# Keep track of all tested configurations
tested_configurations = []

# Hardcoded to use /dev/ttyUSB0
port = "/dev/ttyUSB0"

# Test configurations for only /dev/ttyUSB0
for baudrate in BAUDRATES:
    for parity in PARITIES:
        for databits in DATABITS:
            for stopbits in STOPBITS:
                for ending in BARCODE_ENDINGS:
                    # Combine base barcode data with the ending
                    barcode_data = BASE_BARCODE_DATA + ending
                    configuration = f"Port={port}, Baudrate={baudrate}, Parity={parity}, Data bits={databits}, Stop bits={stopbits}, Ending={ending}"
                    tested_configurations.append(configuration)
                    
                    try:
                        # Configure serial connection with a timeout
                        with serial.Serial(port=port, baudrate=baudrate, parity=parity,
                                           stopbits=stopbits, bytesize=databits, timeout=1) as ser:

                            # Print the current configuration being tested
                            print(f"Testing config: {configuration}")
                            
                            # Send the barcode data with specified ending
                            ser.write(barcode_data)
                            
                            # Wait briefly for the POS to possibly process the data
                            time.sleep(1)

                    except Exception as e:
                        # Print out any errors encountered during the attempt
                        print(f"Failed with {e}")
                    
                    # User input to continue to the next configuration
                    proceed = input("Configuration tested. Press Enter to continue to the next one (or 'N' to stop): ").strip().upper()
                    if proceed == 'N':
                        print("\nExiting early. Tested configurations:")
                        for config in tested_configurations:
                            print(config)
                        exit()  # Exit the script

print("Testing completed.")
