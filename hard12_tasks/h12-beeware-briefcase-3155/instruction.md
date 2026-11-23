You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

iOS auto and menu simulator selection don't work

### Describe the bug

I recently updated to Xcode 27.2, and now Briefcase can't start any simulator except an iPhone Duo.

### How to reproduce the bug

```
(bw-311) msmith@MacBook-Pro apps % briefcase new
[Accept default answers]
(bw-311) msmith@MacBook-Pro apps % cd helloworld 
(bw-311) msmith@MacBook-Pro helloworld % briefcase create ios
...
(bw-311) msmith@MacBook-Pro helloworld % briefcase build ios                                                               

[helloworld] Updating app metadata...
Setting main module... done

[helloworld] Building Xcode project...
Building... done

[helloworld] Built build/helloworld/ios/xcode/build/Debug-iphonesimulator/Hello World.app
(bw-311) msmith@MacBook-Pro helloworld % briefcase run ios                     

Unable to automatically select an iOS simulator; no "SE-class" iPhone simulator (e.g., an iPhone SE, or a similar "entry level" device) is available on iOS 27.2, and the choice is ambiguous.

Specify a device explicitly with -d/--device, or use -d with no value to select from the full list of available simulators.

Log saved to /Users/msmith/git/beeware/apps/helloworld/logs/briefcase.2026_11_14-18_43_18.run.log
```

[briefcase.2026_11_14-18_43_18.run.log](https://github.com/user-attachments/files/34858629/briefcase.2026_11_14-18_43_18.run.log)

```
(bw-311) msmith@MacBook-Pro helloworld % briefcase run ios -d

In the future, you could specify this device by running:

    $ briefcase run iOS -d "iPhone Duo::iOS 27.2"

or:

    $ briefcase run iOS -d 51DD8293-72DF-4BC2-956D-9D261FF9AD07

[helloworld] Starting app on an iPhone Duo running iOS 27.2 (device UDID 51DD8293-72DF-4BC2-956D-9D261FF9AD07)
Opening simulator... done
```

I was never given the option to select a different simulator.

Device Hub shows an iPhone 17e with iOS 27.2, but starting it doesn't make any difference  to this behavior.  Neither can I select it with a `-d` argument:
```
bw-311) msmith@MacBook-Pro helloworld % briefcase run ios -d "iPhone 17e::iOS 27.2"

Invalid device device name 'iPhone 17e'
```

### Environment details

- Operating system and version: macOS 26.7.1
- Python version: 3.11.2
- Software versions:
  - Briefcase: 70d53ad28
