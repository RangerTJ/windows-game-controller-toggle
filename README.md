# hid-toggle

WHAT IS THIS PROGRAM?
---------------------
This program sidesteps issues with certain games where the games themselves are not programmed to handle multiple input devices, even if some devices are unused. Generally, this occurs in games designed around a console-style controller that don't know what to do when they also find other devices plugged in like joysticks, rudder pedals, etc. This program is designed to disable unused devices via software to avoid conflicts and having to unplug/replug devices, which can really mess up painstakingly set up controller bindings in some games.


HOW DOES IT WORK?:
------------------
Assuming you have python 3 installed (and on Windows 10 or higher), you should be able to just place "main.py" and "Toggle Device (run as admin).bat" in the same folder anywhere on your computer. Then, run "Toggle Device (run as admin).bat" as an administrator. This will fire up the python script with elevated privleges so that you can actually enable and disable devices as needed. You can run the .bat or script without it, just you'll get an error when trying to turn stuff on or off (but you can still view the summary of currently plugged in toggle-able devices and their current status).

When prompted by the cmd interface, simply enter 'e' to enable or 'd' to disable, followed by enter! You should get a printout of whether or not the command worked for each affected device, and a summary of device status.


Development Notes:
---------------------------------
Testing Notes:
    *Tested on Windows 10 only
    *Only tested by myself on my own rig

Future Ideas:
    *Disable specific device command
    *Enable specific device command
    *Add UI to make it prettier and not feel like an app from the days of DOS-based adventure games

Disclaimer:
-----------
Files provided as-as, with no support. I'm not liable if you break something! Not that I'd expect it to happen - and anything changed by this script should be fixable manually by just going into Device Manger and manually enabling/disabling affected devices.
