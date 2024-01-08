import serial
import time

# Define the base barcode data here as a byte string
BASE_BARCODE_DATA = b'123456789012'  # Replace with your valid barcode data

# Define possible endings for the barcode: carriage return, newline, or none
BARCODE_ENDINGS = [b'\r', b'\n', b'\r\n', b'']  # CR, LF, CRLF, None

# Define all possible configurations with most common baud rates at the front
BAUDRATES = [
    9600, 19200, 38400, 57600, 115200, 300, 600, 1200, 2400, 4800, 14400, 28800,
    230400, 460800, 921600, 1000000, 1152000, 1500000, 2000000, 2500000, 
    3000000, 3500000, 4000000
]

# Standard parity options
PARITIES = [
    serial.PARITY_NONE,  # Most common
    serial.PARITY_EVEN,  # Common
    serial.PARITY_ODD,   # Common
    serial.PARITY_MARK,  # Less common
    serial.PARITY_SPACE  # Less common
]

# Data bits, typically between 5 and 8
DATABITS = [
    8,  # Most common
    7,  # Less common
    6,  # Rare
    5   # Rare
]

# Stop bits configurations without 1.5
STOPBITS = [
    serial.STOPBITS_ONE,           # Most common
    serial.STOPBITS_TWO            # Less common
]

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
