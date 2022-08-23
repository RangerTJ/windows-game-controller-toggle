@ECHO OFF

ECHO Logging all device information to testStartFull.txt
pnputil /enum-devices > %~dp0\testStartFull.txt

ECHO Logging current HIDclass Devices to %~dp0\testStart.txt
pnputil /enum-devices /class HIDclass > %~dp0\testStart.txt

ECHO Re-Enabling Non-Gamepad Controllers
:: Put any enable commands you want to run here (manually, for the time being) - get this info from the ControllerCheck.bat output.
::pnputil /enable-device "HID\[VID_XXXX&PID_XXXX]\[XXXXXXXXXXXXXXXX]"

ECHO Logging all device information to %~dp0\testDoneFull.txt
pnputil /enum-devices > %~dp0\testDoneFull.txt

ECHO Logging current HIDclass Devices to %~dp0\testDone.txt
pnputil /enum-devices /class HIDclass > %~dp0\testDone.txt

ECHO Non-Gamepad Controllers restored!
PAUSE
