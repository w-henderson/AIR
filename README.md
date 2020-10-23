![AIR Banner](assets/banner.png)
 
# Audio Instant Replay (AIR)

Audio Instant Replay (AIR) is a lightweight and reliable piece of software to create short clips from your microphone at the press of a button. It stores the last 30 seconds (or whatever number you choose) of audio temporarily in RAM until you select the taskbar icon and save a clip. If you've ever used NVIDIA GeForce Experience or any console's clipping functionality, AIR is just like that, but for audio only.

## How do I install it?
1. Clone the repo to your PC.
2. Run `pip install -r requirements.txt` to install AIR's dependencies.
3. Run `start.bat` to open the program in the background.
4. You'll see a message saying that AIR is now running!

## How do I use it?
While AIR is running, you'll see its microphone icon in your taskbar. To make a clip, simply click the taskbar icon or right click and press "Save Clip". You can also exit the program at any time by right-clicking the icon and selecting "Exit". When you save a clip, a file browser will appear to allow you to choose the save location, and once the clip has saved, you'll be notified through a pop-up box.

## How can I change the settings?
The `air.ini` file contains all of the configuration for AIR, and must not be removed. Comment lines begin with a `#`, and configuration variables are in the form `key=value`. At the moment, there are three parameters you can change, of which only one is commonly changed. These are explained below:
| Parameter Name | Default Value | Explaination |
| --- | --- | --- |
| `clipDuration` | `30` | Duration of the clip in seconds. If changed to a value too high, the program could crash due to running out of RAM.
| `device` | `auto` | Select the audio input device. If left on auto, AIR tries to detect a microphone and selects that. Otherwise, enter an integer value that corresponds to the device. You can find said values using the `sounddevice` library's `query_devices()` function.
| `sampleRate` | `44100` | Sample rate to record at. Make sure to choose a value that is supported by your input device. Smaller sample rates will result in lower file size but also lower quality.

## Doesn't this use lots of my PC's resources?
No, not at all. On my PC, with the default configuration values, it doesn't exceed 0.2% CPU usage and 22 MB of RAM when idling.