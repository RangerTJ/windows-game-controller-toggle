# hid-toggle
This program sidesteps issues with certain games where the games themselves are not programmed to handle multiple input devices, even if some devices are unused. Generally, this occurs in games designed around a console-style controller that don't know what to do when they also find other devices plugged in like joysticks, rudder pedals, etc. This program is designed to disable unused devices via software to avoid conflicts and having to unplug/replug devices, which can really mess up painstakingly set up controller bindings in some games. Note: The program/script will need to be run with administrator privledges, since it's method of toggling devices basically amounts to enabling them/disabling them under device manager.

WORK IN PROGRESS: Currently have a working .bat script to pull device summaries t obtain device ID's. Once non-xbox controller style devices are identified, they can be manually input into deactivate/reactivate scripts to turn them on/off seperately. I am currently working to put together a Python script to automate this process, so that you only need to run one application to scan current devices and turn stuff on/off as needed. Currently, you need to set all device ID's manually in the enable/disable .bat files, so they won't do anything out of the box. To use them, uncomment the emable/remove lines, update the device ID paths and repeat as needed if turning on/off multiple devices.

Skeleton code has been uploaded to main.py. Has the core code outline, but has not been tested at all yet and is very, very likely to be broken. Intended to show WIP status, not provide a functional program.... yet!

Known Issues / Development Goals:
---------------------------------
Probably need to revamp parsing stop points / last lines
May be able to greatly simplify parsing of OEMName - check if the actual name always starts at the same char index
    May be index 24, 25, or 26?
Check syntax for \ within a quote to make sure they're used as expected
Need to add actual commands/scripts to run these when starting the app (e.g. prompt for enable/disable/check on boot)
Make sure methods are located where appropriate
Always do a check to build dictionary on program boot
Need to make batch file to call the script that can be run as admin, since admin needed for enable/disable
MAKE SURE X-Box controllers aren't being turned off too
For now: only turn off devices with "HID-compliant game controller" description
    May need helper method to find last char in string if getting index errors or infinite loops with parsing?
FUTURE METHODS:
    Display device summaries (for each dict entry show device name + info)
    Mod to check summary - if error with getting name, just make description + short ID the name
    Disable specific device command
    Enable specific device command

Files provided as-as, with no support. I'm not liable if you break something!
