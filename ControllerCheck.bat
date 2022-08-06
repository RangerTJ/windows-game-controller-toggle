@ECHO OFF

ECHO Logging all device information to %~dp0\DeviceCheck.txt
pnputil /enum-devices > %~dp0\DeviceCheck.txt

ECHO Logging HID controllers ONLY to to %~dp0\ControllerCheck.txt
pnputil /enum-devices /class HIDclass > %~dp0\ControllerCheck.txt

ECHO Logging complete! Have a nice day!
PAUSE