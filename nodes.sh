#! /bin/bash

if [ ! -d  $(pwd)/install ];then
    colcon build
fi
source /opt/ros/iron/setup.sh
source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=/opt/ros/iron/
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
source install/local_setup.bash 
ros2 launch robot launch.xml


