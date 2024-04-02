#! /bin/bash

if [ ! -d  $(pwd)/install ];then
    colcon build
fi
source install/local_setup.bash 
ros2 launch robot launch.xml


