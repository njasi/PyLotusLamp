# PyLotus
This is a simple package to control led lights over bluetooth, as the apps these cheap lights come with are quite undesirable. I dug through a decompilaton of the Lotus lantern X app to make this and then saw someone made their own [app](https://www.reddit.com/r/LedLightStrips/comments/137fh4x/i_didnt_like_the_suggested_app_for_my_led_strips/)... (so I didn't have to dig through that stuff, but it was too late lol).

That said it seems that the LLX app sends diferent codes than that user describes. Most of them still work though (excepting speed command).

## Supported devices
Supposedly any device which would use the "Lotus Lantern X" app (with the execption of the two in one car device I believe; I remember seeing something about it in the decompilation but ignored it at the time).

### Tested devices
- MELK-0C21

## Install
TODO

## Finding Your Bluetooth Mac Address
Various platforms will have their own method of scanning for mac addresses, and this package will eventually have this bundled into the controller, but for now I've included a script that can display the nearby devices:

```sh
python script/scanner.py
```

This just lists all the bluetooth devices your computer can see with some info.


## OS Specific Notes
### MAC OS
Macs may not be able to connect to your device or discover it with the default bluetooth menu. However you can scan for devices with LightBlue & connect to it there. Once connected you can run `system_profiler SPBluetoothDataType` in the terminal to see your connected devices and their addresses.

Note that Mac OS also does not allow pairing through their core bluetooth, so this package will likely not work on mac. `bleak` is used to manage all bluetooth operations, so refer to their docs/issues to see if there is an update on that. You might be able to initiate a connection on your own from the bluetooth menu or with LightBlue.

That being said, I have been able to run a few on/off commands from my mac but it is extremely unpredictable...

...and now it's working with no issues. Don't ask me lol.

### Linux
to test later

### Windows
to test later

### Rasberry Pi
to test later