Arduino Blink Package
=====================

A package for [this](https://aira.readthedocs.io/en/latest/examples/connect_simple_cps.html) lesson

`misc/arduino/arduino.ino` - source code for Arduino board. Upload with IDE or command line.

`rosbag/blink.bag` - objective `QmYYZWNd9esP3YBuuyUBVMH3ymaLDbQFB35S79duYiobcD`

`script/blink.py` - will be called when a new liability will be got

Build
-----

```
$ nix-build release.nix
$ . result/setup.zsh
```

Run
---

```
$ rosrun arduino_blink blink.py
```
