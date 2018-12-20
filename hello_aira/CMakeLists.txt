cmake_minimum_required(VERSION 2.8.3)
project(hello_aira)

find_package(catkin REQUIRED
    COMPONENTS
        rospy
        robonomics_msgs
)

catkin_python_setup()

catkin_package()

catkin_install_python(
    PROGRAMS
        scripts/hello_aira
    DESTINATION
        ${CATKIN_PACKAGE_BIN_DESTINATION}
)
