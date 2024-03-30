#! /bin/bash

if [ ! -d  $(pwd)/install ];then
    colcon build
fi

ros2 launch robot launch.xml
