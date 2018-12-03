cmake_minimum_required(VERSION 2.8.3)
project(arduino_blink)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_package()


## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(
    PROGRAMS
        scripts/blink.py
    DESTINATION
        ${CATKIN_PACKAGE_BIN_DESTINATION}
)
