# == AUDIO INSTANT REPLAY ==
# Developed by William Henderson

# Import required modules
from sounddevice import query_devices
from threading import Thread, Event
from tkinter import filedialog
from PIL import Image
import tkinter as tk
import pystray
import pyaudio
import ctypes
import wave
import sys

# Parse config file
config = {}
with open("air.ini") as f:
    configRaw = f.read()
for line in configRaw.split("\n"):
    if line == "" or line[0] == "#": continue
    keyValue = line.replace(" ","").split("=")
    config[keyValue[0]] = keyValue[1]

# Set up tkinter window then hide it for file dialogs
root = tk.Tk()
root.withdraw()

if config["device"] == "auto":
    # Auto select device by choosing the first device with the word "microphone"
    soundDevices = query_devices()
    selectedMicrophone = None
    for device in soundDevices:
        if "microphone" in device["name"].lower():
            selectedMicrophone = soundDevices.index(device)
            break
    if selectedMicrophone == None:
        ctypes.windll.user32.MessageBoxW(0, "It looks like your device doesn't have a microphone, so AIR cannot start. If this is false, pass the index of your chosen device as a parameter, e.g. `air.exe 2`.", "Error: No microphone", 1)
else:
    selectedMicrophone = int(config["device"])

# Set up audio stream from the microphone
microphone = pyaudio.PyAudio()
sampleRate = int(config["sampleRate"])
clipDuration = int(config["clipDuration"]) # seconds
bufferSize = 882
stream = microphone.open(format=pyaudio.paInt16,channels=1,rate=sampleRate,frames_per_buffer=bufferSize,input_device_index=selectedMicrophone,input=True)
audioFrames = []

def clip():
    # Read frames and store them so they don't change while the user selects the file
    frames = b''.join(audioFrames)

    path = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=(("WAV files", "*.wav"),),
        title="Choose save location"
    )

    if path:
        # Save the audio frames as a wave file
        wf = wave.open(path,"wb")
        wf.setnchannels(1)
        wf.setsampwidth(microphone.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sampleRate)
        wf.writeframes(frames)
        wf.close()
        ctypes.windll.user32.MessageBoxW(0, "Your clip has saved successfully.", "Clip saved", 1)

# End audio capture loop and free microphone
def _exit():
    event.set()
    icon.stop()
    microphone.terminate()
    stream.close()

# Set up the tray icon and its right-click menu 
icon = pystray.Icon("AIR", Image.open("assets/icon.ico"), "AIR", pystray.Menu(
    pystray.MenuItem("Save Clip", clip, default=True),
    pystray.MenuItem("Exit", _exit)
))

# Loop to keep updating the stored audio in memory and make sure its length doesn't exceed the clip duration
def audioCaptureLoop(audioFrames):
    while True:
        audioFrames.append(stream.read(bufferSize))
        if len(audioFrames) > (clipDuration * sampleRate) / bufferSize: del audioFrames[0]
        if event.is_set(): break

# Set up audio capture thread
event = Event()
audioCaptureThread = Thread(target=audioCaptureLoop, args=(audioFrames, ))
audioCaptureThread.start()

ctypes.windll.user32.MessageBoxW(0, "AIR is now running! Click the taskbar icon to make a clip.", "AIR", 1)

# Start the icon loop of checking for icon clicks
icon.run()