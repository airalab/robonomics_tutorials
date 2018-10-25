cmake_minimum_required(VERSION 2.8.3)
project(arduino_with_args)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

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
