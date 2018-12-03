Arduino with Arguments
======================

`misc/arduino/arduino.ino` - source code for Arduino board. Upload with IDE or command line.

`rosbag/blink_blue.bag` - objective `QmUq7d4jATFnbDgtkv83d3VW9jRqqCRkctZdGUBZE5wGN2`
`rosbag/blink_red.bag` - objective `QmcoE93MrvAdC789vt6G27WypSimhZxu5ZT2aKy8uviBDM`

`script/blink.py` - will be called when a new liability will be got

Build
-----

```
$ nix build -f release.nix
$ . result/setup.zsh
```

Run
---

```
$ rosrun arduino_with_args blink.py
```
