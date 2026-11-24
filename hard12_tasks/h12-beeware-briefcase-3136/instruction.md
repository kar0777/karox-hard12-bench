You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Briefcase cannot start a renamed Android emulator

### Describe the bug

Android Studio can rename an emulator, but Briefcase can't handle the resulting configuration.

### Steps to reproduce

Create an emulator in Android Studio (creating it with Briefcase would probably also work). I usually name my emulators after their API levels, so I'll call it "24".

In ~/.android/avd, this creates a a directory 24.avd, and a file 24.ini, which contains the following:
```
avd.ini.encoding=UTF-8
path=C:\Users\smith\.android\avd\24.avd
path.rel=avd\24.avd
target=android-24
```
In the Android Studio Device Manager window, find the emulator, click the pencil icon, and rename it to "24a". This renames 24.ini to 24a.ini, but its content remains the same. 24.avd is *not* renamed, although a couple of lines in 24.avd/config.ini are updated to match:
```
AvdId=24a
avd.ini.displayname=24a
```
After renaming the emulator, Briefcase is no longer able to start it:
```
(bw-dev) smith@xanadu:~/git/beeware/hello$ briefcase run android -v
>>> Android emulator is already installed.

>>> Running Command:
>>>     'C:\Users\smith\Programs\android-sdk\platform-tools\adb.exe' devices -l
>>> Working Directory:
>>>     C:\Users\smith\cygwin\git\beeware\hello
>>> Command Output:
>>>     List of devices attached
>>>
>>> Return code: 0

>>> Running Command:
>>>     'C:\Users\smith\Programs\android-sdk\emulator\emulator.exe' -list-avds
>>> Working Directory:
>>>     C:\Users\smith\cygwin\git\beeware\hello
>>> Command Output:
>>>     21_x86
>>>     21_x86_64
>>>     23_768x1280_64bit
>>>     24a
>>>     28
>>>     33
>>>     beePhone
>>> Return code: 0

Select device:

  1) @21_x86 (emulator)
  2) @21_x86_64 (emulator)
  3) @23_768x1280_64bit (emulator)
  4) @24a (emulator)
  5) @28 (emulator)
  6) @33 (emulator)
  7) @beePhone (emulator)
  8) Create a new Android emulator

> 4

In future, you can specify this device by running:

    $ briefcase run android -d "@24a"

Unable to read configuration of AVD @24a
```

However, if I start it manually in Android Studio, then Briefcase is able to use it:
```
(bw-dev) smith@xanadu:~/git/beeware/hello$ briefcase run android -v
>>> Android emulator is already installed.

>>> Running Command:
>>>     'C:\Users\smith\Programs\android-sdk\platform-tools\adb.exe' devices -l
>>> Working Directory:
>>>     C:\Users\smith\cygwin\git\beeware\hello
>>> Command Output:
>>>     List of devices attached
>>>     emulator-5554          device product:sdk_google_phone_x86_64 model:Android_SDK_built_for_x86_64 device:generic_x86_64 transport_id:14
>>>
>>> Return code: 0

>>> Running Command:
>>>     'C:\Users\smith\Programs\android-sdk\platform-tools\adb.exe' -s emulator-5554 emu avd name
>>> Working Directory:
>>>     C:\Users\smith\cygwin\git\beeware\hello
>>> Command Output:
>>>     24a
>>>
>>>     OK
>>>
>>> Return code: 0

>>> Running Command:
>>>     'C:\Users\smith\Programs\android-sdk\emulator\emulator.exe' -list-avds
>>> Working Directory:
>>>     C:\Users\smith\cygwin\git\beeware\hello
>>> Command Output:
>>>     21_x86
>>>     21_x86_64
>>>     23_768x1280_64bit
>>>     24a
>>>     28
>>>     33
>>>     beePhone
>>> Return code: 0

Select device:

  1) @24a (running emulator)
  2) @21_x86 (emulator)
  3) @21_x86_64 (emulator)
  4) @23_768x1280_64bit (emulator)
  5) @28 (emulator)
  6) @33 (emulator)
  7) @beePhone (emulator)
  8) Create a new Android emulator

> 1

In future, you can specify this device by running:

    $ briefcase run android -d "@24a"

[helloworld] Starting app on @24a (running emulator) (device ID emulator-5554)

[helloworld] Installing app...
```

### Expected behavior

I can think of two possible solutions:
* Instead of going directly to the .android/avd/NAME.avd directory, read .android/avd/NAME.ini first and get the .avd path from there.
* Or, scan all the .avd subdirectories, reading their config.ini files and looking for a matching `AvdId` line.

As far as I can see, the `AvdId` line and the NAME.ini filename are always the same, so I don't know which one is being used by `emulator -list-avds`. 

However, the `displayname` may be different. For example, if I use Android Studio to create an emulator called "23 768x1280 64bit", then I end up with a 23_768x1280_64bit.ini, and a 23_768x1280_64bit.avd/config.ini with the lines:
```
AvdId=23_768x1280_64bit
avd.ini.displayname=23 768x1280 64bit
```
Although the `displayname` is what appears in the Android Studio UI, I don't think we should use it, because Briefcase is a command-line tool and the name with underscores is more convenient.

### Environment

- Operating System: Windows 10
- Python version: 3.8
- Software versions:
  - Briefcase: 891e164576
