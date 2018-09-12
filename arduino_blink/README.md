Arduino Blink
=============

`misc/arduino.ino` - source code for Arduino board. Upload with IDE or command line.

`rosbag/blink.bag` - objective `QmYYZWNd9esP3YBuuyUBVMH3ymaLDbQFB35S79duYiobcD`

`script/blink.py` - will be called when a new liability will be got

Build
-----

```
mkdir -p ws/src && cd ws/src
cp -r path/to/arduino_blink . 
catkin_init_workspace && cd .. && catkin_make 
```
