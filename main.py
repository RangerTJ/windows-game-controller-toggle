# Runs a script to generate a hardware summary text file, then parses the text file to store device information.
# This is then used to run scripts that either enable or disable non-xbox controllers.
# NOTE - THIS CURRENT VERSION HAS NOT BEEN TESTED AND PROBABLY WILL NOT WORK
# (First pass converting pseudo-code to python script - expecting some potential range issues, inefficiencies,
# problems calling MS cmd scripts due to how '\' is handled in quotes, etc.)

import subprocess


class ComputerDevices:
    """
    Represents the controller devices plugged into the computer. Contains a dictionary of devices keyed to their
    Instance ID (containing fields for their status and name).

    Contains methods to derive the ID and Status of a given device from the results of a cmd device list text file
    that results from querying game controllers with the Microsoft PnP Utility.
    """

    def __init__(self):
        self._device_dict = dict()                                  # [0] is Short ID, [1] is device status
                                                                    # [2] is device description, [3] is full name, and
                                                                    # key is the full device Instance ID

    def check_devices(self):
        """
        Runs a batch file that generates a Microsoft PnP Utility report for all HID devices on the PC as a text file.
        Then parses the text file to add each device within it to the device dictionary, keyed to instance ID. The
        first value of the key is the short core device ID, the second is the summary name of the device, the third is
        the status of the device, and the 4th value is the detailed name of the device (optional).

        No parameters and no return. Modifies the class's underlying data directly.
        """

        # subprocess.run('ControllerCheck.bat')                                # If running off external .bat

        # Log device information to ControllerCheck.txt and bring it back in so that we can parse it
        subprocess.run("pnputil /enum-devices /class HIDclass > %~dp0\ControllerCheck.txt")
        controller_summary = open('ControllerCheck.txt')                       # OPEN CONTROLLER SUMMARY TXT
        current_device = None
        for line in controller_summary:
            if "Instance ID" in line:
                device = self._parse_device_check_line(line)
                self._device_dict[device] = [None, None, None, None]
                self._device_dict[device][0] = self._parse_for_short_id(device)
                self._device_dict[device][3] = self._get_name(self._device_dict[device][0])
                current_device = device
            if "Status:" in line:
                status = self._parse_device_check_line(line)
                self._device_dict[current_device][1] = status
            if "Device Description:" in line:
                description = self._parse_device_check_line(line)
                self._device_dict[current_device][2] = description
        controller_summary.close()                                              # CLOSE CONTROLLER SUMMARY TXT

    def disable_controllers(self):
        """
        Runs a command script to disable every controller in the HID device list that is currently started.

        No parameters or returns.
        """

        for device in self._device_dict:
            if device[1] == "disabled":
                disable_cmd = 'pnputil /disable-device ' + device[0] + ' "HID\VID_231D&PID_0201\\7&37d7a043&0&0000"'
                subprocess.run(disable_cmd)
        self.check_devices()

    def enable_controllers(self):  # AKA RESTORE THINGS TO "normal" status
        """
        Runs a command script to disable every controller in the HID device list that is currently started.

        No parameters or returns.
        """

        for device in self._device_dict:
            if device[1] == "disabled":
                enable_cmd = 'pnputil /enable-device ' + device[0] + ' "HID\VID_231D&PID_0201\\7&37d7a043&0&0000"'
                subprocess.run(enable_cmd)
        self.check_devices()

    def _get_name(self, short_id: str) -> str:
        """
        Runs a registry query to using the device's short ID. Generates a text file containing the OEMName, parses it,
        stores it, and returns it, so that it can be added to the device dictionary.

        Parameter "short_id" refers to the short "core" part of the device ID that corresponds to the registry path
        for the device's OEMName (AKA it's actual name that's specific enough to tell what the device actually is).

        Returns the OEM/Full name of the hardware device in question.
        """

        oem_name_query = "reg query HKEY_CURRENT_USER\System\CurrentControlSet\Control\MediaProperties\
                            \PrivateProperties\Joystick\OEM\\" + short_id + " /v OEMName > oem_name.txt"
        subprocess.run(oem_name_query)
        oem_name_txt = open(r'ControllerCheck.txt')
        for line in oem_name_txt:
            if "OEMName" in line:
                char_index = 0
                oem_name = ""
                while line[char_index] is not None:                                 # stops parsing once out of readable chars
                    while line[char_index] == " ":                                  # Advance past initial spaces
                        char_index += 1
                    while line[char_index] != " ":                                  # Advance past OEMname
                        char_index =+ 1
                    while line[char_index] == " ":                                  # Advance past spaces
                        char_index += 1
                    while line[char_index] != " ":                                  # Advance past reg_sz
                        char_index =+ 1
                    while line[char_index] == " ":                                  # Advance past final spaces
                        char_index += 1
                    oem_name = oem_name + line[char_index]                          # Transcribe
                    char_index += 1
                    # IF first two terms/spaces are always set.... maybe just advance a set number of spaces? Also maybe just move it to line 3 (file index of 2) by default?
        oem_name_txt.close()
        return oem_name

    def _parse_device_check_line(self, line: str) -> str:
        """
        Parses a single line of a PnP Utility text file info dump and returns the string that follows the category
        label and empty spaces, so that only the relevant/needed characters of that line are stored in the device
        dictionary.

        Parameter "line" refers to the line to be parsed for it's relevant information.

        Returns the actual data stored on a line without the label and empty spaces.
        """

        device_id = ""
        char_index = 0
        while line[char_index] != ":":                              # Advance until end of label
            char_index += 1
        char_index += 1                                             # Move character to first space after colon
        while line[char_index] == " ":                              # Move character to first char after empty space
            char_index += 1
        while line[char_index] is not None or line[char_index] != " ":
            device_id = device_id + line[char_index]                # Transcribe chars until they stop existing
            char_index += 1
        return device_id

    def _parse_for_short_id(self, line: str) -> str:
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
        return device_id                                            # Return the short ID for the device for use in
                                                                    # retrieving the device's exact name.

# CURRENT EXPECTED ISSUES
# Probably need to revamp parsing stop points / last lines
# May be able to greatly simplify parsing of OEMName - check if the actual name always starts at the same char index
# Check syntax for \ within a quote to make sure they're used as expected
# Need to add actual commands/scripts to run these when starting the app (e.g. prompt for enable/disable/check on boot)
# Make sure methods are located where appropriate
# Always do a check to build dictionary on program boot


# THE PLAN
# Parse Loop:
# -------------
# Before start, create empty device list
# Skip index 0 and 1 move line pointer to row 3 (row index 2)
# While first char != blank [terminate when a header is blank/end of devices]
# ------
# iteration_number = 0
# else:
# ------
# -create new object named device_[iteration number]
# -move line index until it hits colon, then skip spaces until hitting a char that's not a space (or until it hits index 200)
# -if it hits something that's not a space, start transcribing char/moving index up by 1 until it hits a space again
# -move row down 1 and do transcription method, output to description
# -move row down 4 and transcribe method, output to status
# -move row down 3 [puts it on what is either the first line of the new object, or the end if it's blank]
# -append current object to device list
# -iteration_number += 1
#
# Once this is finished
# ---------------------
# create empty dictionary of game controllers
# for each objet in list/dict, if description == "HID-compliant game controller"
# add to dictionary of game controllers keyed to InstanceID
# [needs script] parse the InstanceID and return the chunk between HID\ and \[whatever comes after 2nd slash] to GeneralID (this will be compared against registry check to get actual name of the device)
# for each device in the dictionary, do a registry search/check for the general ID (powershell)
# [needs script] parse the returned data and set the device object's name field to the name that matches from the registry check.