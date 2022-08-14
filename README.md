# hid-toggle

What is this Program and Why does it Exist?
-------------------------------------------
This program sidesteps issues with certain games where the games themselves are not programmed to handle multiple input devices, even if some devices are unused. Generally, this occurs in games designed around a console-style controller that don't know what to do when they also find other devices plugged in like joysticks, rudder pedals, etc. This program is designed to disable unused devices via software to avoid conflicts and having to unplug/replug devices, which can really mess up painstakingly set up controller bindings in some games. Note: The program/script will need to be run with administrator privledges, since it's method of toggling devices basically amounts to enabling them/disabling them under device manager.

THIS PROJECT IS A WORK IN PROGRESS:
-----------------------------------
Currently have a working .bat script to pull device summaries t obtain device ID's. Once non-xbox controller style devices are identified, they can be manually input into deactivate/reactivate scripts to turn them on/off seperately. The WIP Python script automates this process, so that you only need to run one application to scan current devices and turn stuff on/off as needed. Otherwise, you need to set all device ID's manually in the enable/disable .bat files, which won't work unless specific devices are added to enable/disable. To use them as they are, uncomment the emable/remove lines, update the device ID paths and repeat/add extra lines as needed to turn on/off multiple devices. 

The problem here (and why I'm making a project out of this), is that plugging and unplugging devices and other things can change the ID's used to enable/disable devices... which makes doing this manually super tedious (since unplugging a controller to move it means you have to re-do everything by hand again). When finished, the python scrip will handle all the mundane work of refreshing game controller device ID's, identifying them, and making an easy on/off switch without having to tinker with custom batch files and manually parsing device summaries.

Skeleton code has been uploaded to main.py. It currently has the core code outline, but has not been tested at all and I can 99.9% guarantee is broken/non-functional. The upload is intended to show WIP status, not provide a functional program... for now! 

The final program will launch from a .bat file that must be run with admin privleges (to ensure enable/disable calls to pnputil work). This .bat file will launch the actual python program to enable/disable/check game controller devices.


Known Issues / Development Notes:
---------------------------------
May be issues with parsing of OEM Name file (untested)
    
Check syntax for \ within a quote to make sure they're used as expected

Need to add actual command prompt when starting the app (e.g. prompt for enable/disable/check on boot)

Need to build dictionary on program boot
    
FUTURE METHODS:
    *Display device summaries (for each dict entry show device name + info)
    *Mod to check summary - if error with getting name, just make description + short ID the name
    *Disable specific device command
    *Enable specific device command

Files provided as-as, with no support. I'm not liable if you break something!
