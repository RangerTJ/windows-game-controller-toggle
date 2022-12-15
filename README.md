# Windows Game Controller Toggle - ALPHA v 0.2

What is this Program?
---------------------
In short, this program is designed to leave a bluetooth X-Box controller running like normal*, while disabling all other game controllers currently connected to your Windows PC.  

This program sidesteps issues with certain games where the games themselves are not programmed to handle multiple input devices, even if some devices are unused. Generally, this occurs in games designed around a console-style controller that don't know what to do when they also find other devices plugged in like joysticks, rudder pedals, etc. This disables unused devices via software to avoid conflicts and having to unplug/replug devices, which can really mess up painstakingly set up controller bindings in some games (*cough* Star Citizen *cough*). This is basically an automated way of going into Device Manger and right-clicking all the game controllers and disabling or enabling them, but without the tedium or having to guess at vague device descriptions and do it by hand every single time.  

(Also, it lets me put my VKB joysticks sticks in time-out so that my PC can actually go into sleep mode - because apparently that's a thing.)

*Please bear in mind that this is a personal project in alpha status, and has had a relatively small test sample size of tested devices. There are some known first iteration issues. Wired X-box style controllers will currently be disabled/enabled with other devices, since I haven't yet figured a way to filter them out consistently. Blutooth X-Box One controllers will be properly omitted from toggle status, but I haven't tested other bluetooth controllers. Enabling/disabling blutooth controllers that sneak past the filter somehow and show up as toggle-able can cause problems (see warning). While disabling/enabling devices doesn't usally cause issues, there remains the potential for edge cases of complex devices that are actually "multiple" devices logically (such as blutooth controllers), where enabling/disabling them using this approach might prove problematic. Doing so in an earlier version of the program led to a Blue Screen of Death when trying to reconnect the controller. I think because I had "disabled" half of it's tandem devices, while the other half tried to run normally. I suspect the same might have happened by disabling one of the device halves using right-click in settings in device manager, but I haven't been brave enough to test it. While I forsee this program working as intended for the most part, beware there is potental for crashes and driver issues in edge cases.  

WARNING:  

IF A BLUTOOTH CONTROLLER APPEARS IN THE INITIAL CHECK'S TOGGLE-ABLE DEVICE LIST WHEN RUNNING THE PROGRAM, CLOSE THE PROGRAM IMMEDIATELY, DISCONNECT/POWER OFF THE BLUTOOTH CONTROLLER. DO NOT RUN THE PROGRAM UNTIL YOU HAVE DONE THIS.  

If you do run the enable/disable script while a blutooth (and probably any multiple logical device controller), you are likely to get the aforemention blue screen of death crashes when attempting to reconnect the blutooth controller (likely caused by the two logical "devices" for the controller being out of sync). It requires manually fixing the issue to make the device usable again. See "I turned off something and it won't turn back on...", if this occurs.

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
Known Issues:
* My original goal was to have it work on any X-Box style controller (not just blutooth), but it's a bit more complicated than I first anticipated, since there's not any "easy" flags to parse in the device list output without knowing specific device ID's and what they correspond to. All wired controllers that are described as "HID-compliant game controller" will be disabled. To get around this will require profiles/flags and commands to enable/disable only specific devices, which I'd like to implement next. Manual work-around for this is to just have a wired controller unplugged when turning devices off (though this kinda defeats the purpose of having a digital on/off switch - it still helps save keybinds and is generally less involved than unplugging 1+ sim peripherals).

* While I've updated the program to (I believe) ignore toggling blutooth X-Box One controllers, I suggest exercising caution when using it. If your blutooth controller IS detected by the program, make sure that you turn it off and ensure that it doesn't show up in this program's initial device check before enabling or disabling anything. Failure to do so may result in perpetual BSOD issues every time you try to connect it until you clear out all the ghost controller entries in device manager (see "I turned off something and it won't turn back on..."). I might eventually set up an "ignored device list" using static, higher-level device ID's known for specific controllers, but I'd need to find a list of those for all mainstream controllers to do so. With that, I could simply parse devices with those controller ID's out of the enable/disable dictionary.  

* I believe I have a fix implemented now to prevent (at least some) blutooth controllers from showing up. As of right now, it's only been tested on my own x-box one blutooth controller and relies on an assumption about blutooth controllers having "{}" brackets in their Instance ID, which I cannot verify is the case 100% of the time, as of yet. In the case of my official X-Box blutooth controller, there appears to be at least 2 different devices that show up for it (both a blutooth x-input and game controller). The first iteration of this program disabled the game controller part and ignored the x-input part, and I suspect this is related to what caused the BSOD crashes. The game controller's Instance ID used brackets that appeared to reference the related x-input device, so the current fix is to just take any device with "{}" brackets in its Instance ID out of consideration for toggle-able status, since this appears to be a nomenclature used in pairing more complex controller setups. My current operating assumption is that brackets are used to reference the Instance ID of a blutooth controller. As a disclaimer, I have been unable to find documentation on this as of yet (so this assumption is based on observation of device ID's on my home PC). It appears to resolve the issue in at least the case of my own X-Box One controller, at least.  

* Tested by myself on Windows 10 Pro only.  

* There are edge cases where you won't get a specific OEM name (the detailed / accurate name) for a device due to where the key is stored in the registry. I speifically designed this app around my own usage case of dual VKB joysticks and CH rudder pedals based on where their OEMName registry keys were found. I noticed some of my old Thrustmaster stuff that I'd used a while back had keys in different locations (and possibly didn't even have OEM name keys). It would take a lot of work to track down edge cases, and since this aspect isn't *super* essential to the program, anythingthat doesn't get a neat, clean OEM name will just be assigned a combo of the description + short ID as it's placeholder name. This should be functional enough for edge cases to at least get some idea of what device they represent.  

* Original intent was for text parse files to stay in the same folder as the python script and bat file (which is what happens when runing main.py or the .bat normally), but Windows is dumping them into the System32 folder when the script is launched from the .bat file as an admin. It works fine, but I don't particularly like messing with stuff in the system folders if it can be avoided. Current files placed here are: ControllerCheck.txt and oem_name.txt, just FYI. I may look into alternative locations to store them that can use a dynamic filepath (like a new folder within the current user's documents folder or something similar).  
    

Future Ideas:

    * Parse shell commmand output entirely within python script, so no text file output is necessary
    * Disable specific device command  
    * Enable specific device command  
    * Add GUI to make it prettier and not feel like an app from the days of DOS-based adventure games  
    * Ways to customize enable/disable profiles  
    * EXE file/installer to make things a bit cleaner / make it pinnable to taskbar  
    

"I turned off something and it won't turn back on..."
-----------------------------------------------------
While testing my first version of this app, I disabled my blutooth X-Box One controller. Apparently this made Windows very mad and resulted in a blue screen of death every time I attempted to connect the controller. If you see a "need to restart for this change to take effect" type message pop up while running this program, this means something complex probably got messed with and you'll likely have to follow the link's suggestion to fix it. Or a system rollback. It may not hurt to make new restore point just before running this the fist time, just in case you need to reset hardware status after enabling/disabling anything. A glowing endorsement by the author, I know, heh. I resolved this following the suggestions on this post (top answer):  

https://answers.microsoft.com/en-us/windows/forum/all/bsod-loop-after-installing-xbox-controller-drivers/31f3875c-0fd0-499d-9e86-788c666ce3f5  

Removing all the hidden HID and and phantom blutooth x-box controllers and forcing the controller to re-pair with Windows seemed to do the trick and I got mine working again in ~1 hr (could do it in minutes now that I know what worked... or so I tell myself). I strongly suggest *not* using this program to enable or disable *anything* as long as a blutooth controller is active/paired. If you see one (or a device you suspect is one) on the check summary before you enable/disable the rest of your devices, make sure to close the program out completely and turn off your blutooth controller, as a work-around. I believe I now have a fix in place so taht this won't be necessary, but I cannot guarantee that it will work on all devices (since I have tested exactly *one* device).  

Anything *else* changed by this program should be fixable manually by just going into Device Manger and manually enabling/disabling affected devices. I don't think this should be an issue at all, but on the off chance it turns devices off and you can't get them to turn back on, just go to device manager, find the disabled device (likely under Human Interface Devices), right-click the disabled device and click "Enable Device" from the drop-down menu.  


Change Log
----------
12/14/22: Fixed issue that resulted in the .bat file failing to load in certain directories (basically any directory other than the one initially tested).
8/24/22: X-Box One blutooth controllers *should* no longer show up in the list of devices that can be enabled/disabled. This is to prevent accidentally disabling the device and having to deal with resulting BSOD issues that linger when trying to connect the controller until corrupted/phantom devices are purged from device manager.  
