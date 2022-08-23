# Windows Game Controller Toggle

What is this Program?
---------------------
In short, this program is designed to leave an X-Box controller running like normal, while disabling all other game controllers currently connected to your Windows 10 PC (and probably Windows 11 too, assuming the console commands are the same).

This program sidesteps issues with certain games where the games themselves are not programmed to handle multiple input devices, even if some devices are unused. Generally, this occurs in games designed around a console-style controller that don't know what to do when they also find other devices plugged in like joysticks, rudder pedals, etc. This program is designed to disable unused devices via software to avoid conflicts and having to unplug/replug devices, which can really mess up painstakingly set up controller bindings in some games. This is basically an automated way of going into Device Manger and right-clicking all the game controllers and disabling or enabling them, but without the tedium or having to guess at vague device descriptions and do it by hand every single time.


How Does it Work?
------------------
Assuming you have python 3 installed (and on Windows 10 or higher), you should be able to just place "main.py" and "Toggle Device (run as admin).bat" in the same folder anywhere on your computer. Then, run "Toggle Device (run as admin).bat" as an administrator. This will fire up the python script with elevated privleges so that you can actually enable and disable devices as needed. You can run the .bat or script without it, just you'll get an error when trying to turn stuff on or off (but you can still view the summary of currently plugged in toggle-able devices and their current status).

When prompted by the cmd interface, simply enter 'e' to enable or 'd' to disable, followed by enter! You should get a printout of whether or not the command worked for each affected device, and a summary of device status.


Development Notes
-----------------

-Tested by myself on Windows 10 only

-There are probably edge cases where you won't get a specific OEM name (the detailed / accurate name) for a device due to where the key is stored in the registry. I speifically designed this app around my own usage case of dual VKB joysticks and CH rudder pedals based on where their OEMName registry keys were found. I noticed some of my old Thrustmaster stuff that I'd used a while back had keys in different locations (and possibly didn't even have OEM name keys). It would take a lot of work to track down edge cases, and since this aspect isn't *super* essential to the program, anythingthat doesn't get a neat, clean OEM name will just be assigned a combo of the description + short ID as it's placeholder name. This should be functional enough for edge cases to at least get some idea of what device they represent.

-I believe that most x-box style controllers should be skipped by this app (as intended). My own blutooth X-Box One controller shows up with the description of "Bluetooth XINPUT compatible input device" so I am currently operating off the assumptiont that controller style xinput devices are similarly described. That said, if for some reason their official description is "HID-compliant game controller" this program WILL treat them like a joystick and enable/disable them, as this is the filter I use to detect joysticks, rudder pedals, etc. for enable/disable elgibility (along with filtering out disonnected devices). My gut says a PS4 controller is a likely canidate to get caught by the program and treated like a joystick instead of a console controller.

-The prior long-winded point is why I'd also like to eventually set up a way to enable/disable specific devices, in case the one-size-fits-most approach doesn't work in some cases.
    

Future Ideas:

    -Disable specific device command
    -Enable specific device command
    -Add UI to make it prettier and not feel like an app from the days of DOS-based adventure games
    -Ways to customize enable/disable profiles
    

"I turned off something and it won't turn back on..."
-----------------------------------------------------
Anything changed by this program should be fixable manually by just going into Device Manger and manually enabling/disabling affected devices. I don't think this should be an issue at all, but on the off chance it turns devices off and you can't get them to turn back on, just go to device manager, find the disabled device (likely under Human Interface Devices), right-click the disabled device and click "Enable Device" from the drop-down menu.
