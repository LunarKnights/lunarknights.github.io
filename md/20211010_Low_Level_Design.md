## Agenda

1. Recap
2. Misc Topics
3. C/C++ Lunar Knights Library Design

## Misc Topics

These are some topics we discussed in relation to making design choices. Feel free to research any of them or ask me questions.

- Functional vs Object-Oriented Programming
- Public vs Private Members
- "There should be one - and preferably only one - obvious way to do it." From the [Zen of Python](https://www.python.org/dev/peps/pep-0020/)

## C/C++ Lunar Knights Library Design

We started writing up a formalize design document for the entire Lunar Knights codebase. The design doc will be located [here](/docs/design.html).

### Hardware

#### DC Motors

5 bag motors controlled by the TalonSRXs. Four motors will be used on the base of motion subsystem. One motor will be used on the intake system.

Each motor will be represented by a `Motor` class. This class will create a `TalonSRX` object and will have the following attributes:

```c
set_power(float power) -> void
get_ticks(void) -> int
get_current(void) -> float

reset_ticks(void) -> void
reverse(void) -> bool
```

#### Stepper Motor

2 stepper motors controlled by TBD. Two motors will be used on the intake system to raise and lower the bucket system.

Each stepper will be represented by a `Stepper` class. 

```c
private int steps

step_by(int number) -> void
 - step_c
 - step_cc
get_steps(void) -> int

reset_steps(void) -> void
```

#### Encoders

2 encoders will be used on the intake lead screws.

Each encoder is represented by an `Encoder` class.

```c
get_ticks(void) -> void
reset_ticks(void) -> void
```

#### IMU

1 IMU will be used to track the robots heading.

```c
get_heading(void) -> float
get_yaw(void) -> float
get_roll(void) -> float

reset(void) -> void
```

#### Camera Device

1 ZED Camera will be used. Due to GPU limitations with the ZED SDK and the raspberry pi, we will need to write our own Camera API using OpenCV. If we switch to the Jetson Nano, we will be able to use the existing ZED SDK.

```c
get_frame(void) -> Image
get_depth(void) -> Image
```

### Subsystems

#### Base of Motion

The base includes 4 dc motors and 1 imu.

```c
init(void) -> bool

// teleop controls
set_left_power(float) -> void
set_right_power(float) -> void

move(int) -> void
turn(float) -> void

// we must have a thread to track pos
get_position(void) -> (float, float)
```

#### Intake

The intake includes 2 steppers, 1 dc motor, and 2 encoders.

```c
init(void) -> bool

mine(void) -> bool
 - does everything below automatically

dig(void) -> bool
lower(void) -> bool
raise(void) -> bool

stop(void) -> bool
```

#### Deposition

The deposition includes TBD.

```c
init(void) -> bool

dump(void) -> bool
```

