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
PORT = "/dev/ttyUSB0"

def test_configuration(port, baudrate, parity, databits, stopbits, ending):
    try:
        # Get printable representation of barcode ending
        ending_str = repr(ending.decode('utf-8'))
        configuration = f"Port={port}, Baudrate={baudrate}, Parity={parity}, Data bits={databits}, Stop bits={stopbits}, Ending={ending_str}"

        # Configure serial connection with a timeout
        with serial.Serial(port=port, baudrate=baudrate, parity=parity,
                           stopbits=stopbits, bytesize=databits, timeout=1) as ser:

            # Combine base barcode data with the ending
            barcode_data = BASE_BARCODE_DATA + ending
            
            print(f"Testing config: {configuration}")

            ser.write(barcode_data)
            
            # Wait briefly for processing
            time.sleep(1)

            tested_configurations.append(configuration)

    except Exception as e:
        print(f"Configuration {configuration} failed with error: {e}")

def main():
    for baudrate in BAUDRATES:
        for parity in PARITIES:
            for databits in DATABITS:
                for stopbits in STOPBITS:
                    for ending in BARCODE_ENDINGS:
                        test_configuration(PORT, baudrate, parity, databits, stopbits, ending)
                        
                        # User input to continue to the next configuration
                        proceed = input("Configuration tested. Press Enter to continue to the next one (or 'N' to stop): ").strip().upper()
                        if proceed == 'N':
                            print("\nExiting early. Tested configurations:")
                            for config in tested_configurations:
                                print(config)
                            return
    print("Testing completed.")

if __name__ == "__main__":
    main()