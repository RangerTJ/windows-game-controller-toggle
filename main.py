# Author: Raptor2k1
# Date: 12/14/2022

# Description:  Uses Microsoft PNP Utility commands to generate a dictionary of plugged-in devices categorized
#               as game controllers and uses registry queries to attempt to find a more detailed OEM Name for
#               the device (if it's available in the joystick directory of the registry). Dictionary objects are then
#               used as references to either enable all or disable all plugged-in devices.

# Note:         This script must be run with elevated (admin) privileges to support device enabling/disabling.
#               X-Box style controllers have a different description and should not be turned on/off by this
#               program. The primary goal is to turn other peripherals (usually sim controllers) on/off as needed
#               without screwing up key bindings or dealing with physically plugging in/unplugging devices.

import subprocess


class InterfaceDevice:
    """
    Represents a controller device tied to the computer. Contains data members for the device Instance ID, short ID,
    description, and OEM name (all stored as strings). All initialized as empty strings, until they are set.

    Contains methods to set and get all data members.
    """

    def __init__(self):
        self._instance_id = ""
        self._short_id = ""
        self._description = ""
        self._status = ""
        self._oem_name = ""

    # Set methods for all data members of a device object
    def set_instance_id(self, instance_id: str):
        self._instance_id = instance_id

    def set_short_id(self, short_id: str):
        self._short_id = short_id

    def set_description(self, description: str):
        self._description = description

    def set_status(self, status: str):
        self._status = status

    def set_oem_name(self, oem_name: str):
        self._oem_name = oem_name

    # Get methods for the device object's data members
    def get_instance_id(self):
        return self._instance_id

    def get_short_id(self):
        return self._short_id

    def get_description(self):
        return self._description

    def get_status(self):
        return self._status

    def get_oem_name(self):
        return self._oem_name


class ControllerCollection:
    """
    Represents the controller devices plugged into the computer. Contains a dictionary of devices keyed to their
    Instance ID (containing fields for their status and name).

    Contains methods to derive the ID and Status of a given device from the results of a cmd device list text file
    that results from querying game controllers with the Microsoft PnP Utility.
    Has helper methods to assist in parsing text file data.
    Also has a method to print a quick summary of toggle-able devices and whether they are Started or Disabled.
    """

    def __init__(self):
        self._device_dict = dict()

    def check_devices(self):
        """
        Runs a batch file that generates a Microsoft PnP Utility report for all HID devices on the PC as a text file.
        Then parses the text file to add each device within it to the device dictionary, keyed to instance ID. The
        first value of the key is the short core device ID, the second is the summary name of the device, the third is
        the status of the device, and the 4th value is the detailed name of the device (optional).

        No parameters and no return. Modifies the class's underlying data directly.
        """

        # Use pnputil command to get summary of all HID class devices detected by the PC and store in txt file
        print("Capturing controller information...")
        controller_summary = subprocess.run("pnputil /enum-devices /class HIDclass", capture_output=True, text=True)
        controller_summary_lines_table = controller_summary.stdout.splitlines()

        # Open HID device summary txt file in read mode and parse it
        device = None

        for line in controller_summary_lines_table:

            if "Instance ID" in line:
                device = self._parse_device_check_line(line)                    # Create object keyed to instance ID
                self._device_dict[device] = InterfaceDevice()                   # Set instance ID and short ID
                self._device_dict[device].set_instance_id(device)
                self._device_dict[device].set_short_id(self._parse_for_short_id(device))
            if "Status:" in line:                                               # Set status
                status = self._parse_device_check_line(line)
                self._device_dict[device].set_status(status)
            if "Device Description:" in line:                                   # Set description
                description = self._parse_device_check_line(line)
                self._device_dict[device].set_description(description)

        # Clear non-controller devices from the dictionary
        del_list = []
        for device in self._device_dict:                                        # Filter out irrelevant or bluetooth
            if self._device_dict[device].get_description() != "HID-compliant game controller" or \
                    self._device_dict[device].get_status() == "Disconnected" or \
                    "{" in self._device_dict[device].get_instance_id():
                del_list.append(device)
        for device in del_list:                                                 # Delete everything in delete list
            self._device_dict.pop(device)

        # Get OEM Names for any game controllers that remain
        for device in self._device_dict:
            self._device_dict[device].set_oem_name(self._get_name(self._device_dict[device]))

    def disable_controllers(self):
        """
        Runs a command script to disable every game controller in the HID device list that is currently started.

        No parameters or returns.
        """

        for device in self._device_dict:
            if self._device_dict[device].get_status() == "Started":
                disable_id = self._device_dict[device].get_instance_id()
                disable_cmd = 'pnputil /disable-device ' + '"' + disable_id + '"'
                subprocess.run(disable_cmd)
        self.check_devices()

    def enable_controllers(self):
        """
        Runs a command script to enable every game controller in the HID device list that is currently disabled.

        No parameters or returns.
        """

        for device in self._device_dict:
            if self._device_dict[device].get_status() == "Disabled":
                enable_id = self._device_dict[device].get_instance_id()
                enable_cmd = 'pnputil /enable-device ' + '"' + enable_id + '"'
                subprocess.run(enable_cmd)
        self.check_devices()

    def summarize_game_controllers(self):
        """
        Prints the currently-detected toggle-able controllers and their status.

        No parameters or returns.
        """

        print("\nStatus of Plugged-in Game Controllers:"
              "\n--------------------------------------")
        for device in self._device_dict:
            status = self._device_dict[device].get_status()
            name = self._device_dict[device].get_oem_name()
            print(name + ": " + status)

    def _get_name(self, device: object) -> str:
        """
        Runs a registry query to using the device's short ID. Generates a text file containing the OEMName, parses it,
        stores it, and returns it, so that it can be added to the device dictionary.

        Parameter "short_id" refers to the short "core" part of the device ID that corresponds to the registry path
        for the device's OEMName (AKA it's actual name that's specific enough to tell what the device actually is).

        Returns the OEM/Full name of the hardware device in question.
        """

        # Capture OEM name if it's a joystick with its OEM Name in the joystick section of the registry
        device_id = device.get_short_id()
        description = device.get_description()
        oem_name_query = 'reg query "HKEY_CURRENT_USER\System\CurrentControlSet\Control\Media' \
                         'Properties\PrivateProperties\Joystick\OEM\\' + device_id + '" ' + '/v OEMName'
        oem_name = subprocess.run(oem_name_query, capture_output=True, text=True)
        oem_name_lines_table = oem_name.stdout.splitlines()

        # When there's an error finding the target registry key for an OEM Name, assign placeholder name
        if "ERROR" in oem_name_lines_table[0]:
            return str(description + ": " + device_id)

        # If an actual OEM name is found, parse it and assign it
        else:
            target_line = oem_name_lines_table[2]
            oem_name = self._parse_oem_name(target_line)
            print(oem_name)
            return oem_name

    @staticmethod
    def _parse_oem_name(line: str) -> str:
        """
        Parses line 2 of the OEM name reg query results, which should look like:
        "    OEMName    REG_SZ     DEVICE NAME HERE  "

        Takes line a string (intended to be line 2 of the reg query output text file) as a parameter.

        Returns the actual device name portion of line 2 as a string, so it can be used by the _get_name method.
        """

        # Initialize char index tracker and blank string to build on
        char_index = 0
        oem_name = ""
        length = len(line)

        # Iterate through line 2 of oem_name.txt and transcribe the important part and return it
        while line[char_index] == " ":                              # Skip over first blank spaces
            char_index += 1
        while line[char_index] != " ":                              # Skip over "OEMName" text
            char_index += 1
        while line[char_index] == " ":                              # Skip over second blank spaces
            char_index += 1
        while line[char_index] != " ":                              # Skip over "REG_SZ"
            char_index += 1
        while line[char_index] == " ":                              # Skip over third blank spaces
            char_index += 1
        while char_index < length:                                  # Transcribe until chars stop
            oem_name = oem_name + line[char_index]
            char_index += 1
        return oem_name

    @staticmethod
    def _parse_device_check_line(line: str) -> str:
        """
        Parses a single line of a PnP Utility text file info dump and returns the string that follows the category
        label and empty spaces, so that only the relevant/needed characters of that line are stored in the device
        dictionary.

        Parameter "line" refers to the line to be parsed for its relevant information.

        Returns the actual data stored on a line without the label and empty spaces.
        """

        length = len(line)
        device_id = ""
        char_index = 0
        while line[char_index] != ":":                              # Advance until end of label
            char_index += 1
        char_index += 1                                             # Move character to first space after colon
        while line[char_index] == " ":                              # Move character to first char after empty space
            char_index += 1
        while char_index < length:                                  # Transcribe chars until they stop existing
            device_id = device_id + line[char_index]
            char_index += 1
        return device_id

    @staticmethod
    def _parse_for_short_id(line: str) -> str:
        """
        Returns the "short" ID for a device, that can then be plugged into a command to return parsable
        data to identify the specific name of the device in the Instance ID key (since it is not output with
        the PnP Utility summary and requires a separate shell command to retrieve and parse).

        Parameter "line" refers to the line to be parsed for the short ID. Likely to be the key stored in the device
        dictionary to avoid having to waist iterations re-parsing an entire additional text file.

        Returns the usable short ID as a string.
        """

        device_id = ""
        char_index = 0
        while line[char_index] != "\\":                             # Move pointer until it finds a '\' character
            char_index += 1
        char_index += 1                                             # Move pointer to first char within slash section
        while line[char_index] != "\\":                             # Transcribe everything prior to the next '\'
            device_id = device_id + line[char_index]
            char_index += 1
        return device_id                                            # Return short ID for getting exact device name


# Start up script - populate the device dictionary
my_devices = ControllerCollection()
my_devices.check_devices()
my_devices.summarize_game_controllers()

# Prompt the user for a decision
decision = input("Input 'e' to enable devices or 'd' to disable devices. Input any other value to quit.\n"
                 "Select choice and hit Enter to confirm: ")
if decision == "e":
    my_devices.enable_controllers()
    my_devices.summarize_game_controllers()
elif decision == "d":
    my_devices.disable_controllers()
    my_devices.summarize_game_controllers()

# Additional functionality to keep window open long enough / pause closing until key pressed
input("\nProcess Complete! Press 'Enter' to exit the program.")
