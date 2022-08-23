# Windows Game Controller Toggle

What is this Program?
---------------------
In short, this program is designed to leave an X-Box controller (controller with a description of XINPUT compatible input device) running like normal*, while disabling all other game controllers currently connected to your Windows PC.

WARNING: DO NOT ATTEMPT TO ENABLE OR DISABLE DEVICES WHILE A BLUTOOTH CONTROLLER IS CONNECTED. ISSUE FOUND WHERE THIS CAN LEAD TO BLUE SCREEN OF DEATH WHEN TRYING TO RECONNECT THE CONTROLLER.

This program sidesteps issues with certain games where the games themselves are not programmed to handle multiple input devices, even if some devices are unused. Generally, this occurs in games designed around a console-style controller that don't know what to do when they also find other devices plugged in like joysticks, rudder pedals, etc. This disables unused devices via software to avoid conflicts and having to unplug/replug devices, which can really mess up painstakingly set up controller bindings in some games (*cough* Star Citizen *cough*). This is basically an automated way of going into Device Manger and right-clicking all the game controllers and disabling or enabling them, but without the tedium or having to guess at vague device descriptions and do it by hand every single time.

Also, it lets me put my VKB joysticks sticks in time-out so that my PC can actually go into sleep mode.

*Currently some first iteration issues - most X-box style controllers will be disabled/enabled with other devices. See work-around for blutooth/wireless controllers in "How Does it Work? / Development Notes. Wired controllers will probably have to wait for profile support.

How Does it Work?
------------------
Just place "main.py" and "Toggle Device (run as admin).bat" in the same folder anywhere on your computer (a non-admin folder is probably ideal). Then, run "Toggle Device (run as admin).bat" as an administrator. This will fire up the python script with elevated privleges so that you can actually enable and disable devices as needed. You can run the .bat or script without it, just you'll get an error when trying to turn stuff on or off. You can still view the summary of currently plugged in toggle-able devices and their current status, but that's it without admin privleges. Since this requires admin rights, I encourage you to check out the source code, so you can be sure that everything is kosher. Note that with current implementation, even an official wireless X-Box controller is getting picked up as a joystick for the mass enable/disable. If you have a blutooth controller you can currently work around this by not turning the controller on until joysticks are disabled, when disabling devices.

When prompted by the cmd interface, simply enter 'e' to enable or 'd' to disable, followed by enter! You should get a printout of whether or not the command worked for each affected device, and a summary of device status.


Requirements
------------

Windows 10

Python 3.10 (https://www.python.org/downloads/)


There is a fair chance this will work on Windows 11 too, unless commands have changed.
May work on earlier versions of Python 3, but no guarantees.


Development Notes
-----------------
-Current Priority Issue: ALL Controllers that are described as "HID-compliant game controller" will be disabled (currently happening to my own blutooth X-Box One Controller). To get around this will require profiles/flags and commands to enable/disable only specific devices, which I'd like to implement next. Oddly, disabling the blutooth-connected X-Box controller didn't disable it right away (recieved a message about requiring a restart before it would take effect... and I'm pretty sure this is related to the BSOD I'm getting when trying to re-connect it not). Current work-around is to just not turn on any blutooth controllers until after flight sticks are disabled, so they don't get caught in the crossfire.

-Tested by myself on Windows 10 only

-There are edge cases where you won't get a specific OEM name (the detailed / accurate name) for a device due to where the key is stored in the registry. I speifically designed this app around my own usage case of dual VKB joysticks and CH rudder pedals based on where their OEMName registry keys were found. I noticed some of my old Thrustmaster stuff that I'd used a while back had keys in different locations (and possibly didn't even have OEM name keys). It would take a lot of work to track down edge cases, and since this aspect isn't *super* essential to the program, anythingthat doesn't get a neat, clean OEM name will just be assigned a combo of the description + short ID as it's placeholder name. This should be functional enough for edge cases to at least get some idea of what device they represent.

-Original intent was for text parse files to stay in the same folder as the python script and bat file (which is what happens when runing main.py or the .bat normally), but Windows is dumping them into the System32 folder when the script is launched from the .bat file as an admin. It works fine, but I don't particularly like messing with stuff in the system folders if it can be avoided. Current files placed here are: ControllerCheck.txt and oem_name.txt, just FYI. I may look into alternative locations to store them that can use a dynamic filepath (like a new folder within the current user's documents folder or something similar).
    

Future Ideas:

    -Disable specific device command
    -Enable specific device command
    -Add UI to make it prettier and not feel like an app from the days of DOS-based adventure games
    -Ways to customize enable/disable profiles
    

"I turned off something and it won't turn back on..."
-----------------------------------------------------
Anything changed by this program should be fixable manually by just going into Device Manger and manually enabling/disabling affected devices. I don't think this should be an issue at all, but on the off chance it turns devices off and you can't get them to turn back on, just go to device manager, find the disabled device (likely under Human Interface Devices), right-click the disabled device and click "Enable Device" from the drop-down menu.
