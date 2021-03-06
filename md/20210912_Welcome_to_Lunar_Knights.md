## Agenda

1. Introductions
2. Software Status
3. Sub-groups
4. Potential Workshop Topics

## LK Software

Welcome to the cool side of Lunar Knights. The software subteam is primarily responsible for the remote and autonomous operation of the robot. We also are in charge of maintaining low-level hardware apis and high-level robot health monitors. We cover a broad range of "computer science" topics such as: control systems, computer vision, machine learning, frontend, backend, and networking.

## Status of LK Software

As of Spring 2020, we have basic robot controls that is consistent with mechanical progress. We can drive the LK robot chasis around using a gamepad connected to an external device.

This means we have:

-   Talon SRX motor controls
-   Tele-op controls over WiFi
-   Basic dashboard for robot health (aka motor current and gamepad inputs)

We have separated the code base into three main parts:

1. Low level C++ library for basic hardware and robot controls
2. Python module for controlling the robot and starting the primary server
3. Python/Js client for sending/getting robot info

## Sub-groups

Although we have needs in many areas, we do not expect everyone to be fully active in every part. We are introducing sub-groups to better organize tasks. Everyone who wants to be on the "software team" will have a chance to participate in any these groups.

-   LK Library
    -   Super low level (Talons, i2c, can) mostly provided by external services
    -   Low level library, C/C++, (primary hardware api, general motor controls, sensor reads)
    -   High level, C/C++/Python, (primary robot api, subsystem controls)
    -   _Interested in_:
        -   producing libraries
        -   hardware software link
        -   electrical side
-   LK Robot
    -   Controls, Python, (Teleop, autonomous systems)
    -   Health UI, Python/Js/React, (console, motors, gamepad)
    -   _Interested in_:
        -   frontend/backend/full stack/web dev
        -   motion planning/obstacle avoidance
        -   computer vision
        -   "traditional FIRST robotics" programming

## Workshops

Lunar Knights will host short workshops on various topics. These are subject to change. If you want a workshop on a topic not listed OR if you would like to lead a workshop on a topic, let me know.

-   Development tools
    -   Git
    -   Docker
    -   text editors
-   C/C++ Crash Course
-   Python Fun
-   Computer vision topics
    -   Image kernels
    -   Stereo images
    -   Motion
    -   CNNs
-   Machine learning topics
-   Autonomous systems
    -   PIDs
    -   Robot tracking
-   ROS 2 / Gazebo
