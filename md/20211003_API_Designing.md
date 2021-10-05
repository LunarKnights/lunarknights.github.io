## Agenda

1. Recap
2. C in Python Demo
3. Previous control systems work
3. Design Discussions
4. Preparing for Next Week

## C in Python Demo

For low-level programming we will use C/C++; however, for higher tasks (such as the dashboard), we will use Python. 

### Dependencies

Some C compiler such as `gcc` or `clang`. Your system probably already has one installed, but if not look up C compiler install instructions for your machine.

Python 3: [https://www.python.org/downloads/](https://www.python.org/downloads/)

Install the `cffi` package for python: `python3 -m pip install cffi`

### Sample Shared C Library

We will use the foreign function interface (FFI) to call C functions in Python. Let's first create a C library.

Consider a header file such as:

```c #
void hello(void);
int adder(int x, int y);
```

And an implementation:

```c #
void hello(void) {
	printf("Hello from C!\n");
}

int adder(int x, int y) {
	return x + y;
}
```

Compile the demo shared library:

```sh
gcc -shared -o libdemo.so -fPIC src/demo.c
```

#### `ctypes` module

Documentation: [https://docs.python.org/3/library/ctypes.html](https://docs.python.org/3/library/ctypes.html) 

```python #
from ctypes import CDLL
lib = CDLL('./libdemo.so')
lib.hello()
print('result', lib.adder(2, 3))
```

**Pros:** included in the standard Python modules

**Cons:** requires casting Python to C types for many data types

#### `cffi` module

Documentation: [https://cffi.readthedocs.io/](https://cffi.readthedocs.io/)

```python #
from cffi import FFI

ffi = FFI()
ffi.cdef('''
void hello(void);
int adder(int x, int y);
''')

lib = ffi.dlopen('./libdemo.so')

lib.hello()

print('result', lib.adder(2, 3))
```

**Pros:** easier to deal with types

**Cons:** requires an external import

### Sample C Extensions module

Documentation: [https://docs.python.org/3/extending/extending.html](https://docs.python.org/3/extending/extending.html)

The source c file should look like this:

```c #
static PyObject *hello(PyObject *self, PyObject *args) {
	printf("Hello from C!\n");
	return Py_None;
}

static PyObject *adder(PyObject *self, PyObject *args) {
	int x, y;
	if (!PyArg_ParseTuple(args, "ii", &x, &y)) return NULL;

	return PyLong_FromLong(x + y);
}

static PyMethodDef DemoMethod[] = {
	{"hello", hello, METH_VARARGS, "hello"},
	{"adder", adder, METH_VARARGS, "adder"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef demomod = {
	PyModuleDef_HEAD_INIT,
	"demo",
	NULL,
	-1,
	DemoMethod
};

PyMODINIT_FUNC PyInit_demo(void) {
	return PyModule_Create(&demomod);
}
```

To build this module create a `setup.py` file:

```python #
from distutils.core import setup, Extension

module = Extension('demo', sources=['src/demomod.c'])

setup(name='Demo Module',
    version='0.1',
    description='Demo extension',
	ext_modules=[module])
```

Compile the module with:

```sh
python3 setup.py build --build-lib=.
```

Now we can use the C extension in python:

```python #
import demo

demo.hello()
print('result', demo.adder(2, 3))
```

### Run the demos

```sh
python3 ctypes_demo.py
python3 cffi_demo.py
python3 cext_demo.py
```

Each script should produce an output similar to:

```console
Hello from C!
Python: 5
```

Run `python3 speed_demo.py` to see the speed of each method.

Sample output:

```console
Loading ctypes.CDLL took 0.012s
Loading cffi.FFI took 0.045s
Loading c extension took 0.004s

Running adder for 20,000,000 iterations...
ctypes took 3.146s
cffi took 2.720s
cext took 1.384s
```

## Previous control systems work

You had to be there, but we demonstrated the previous robot dashboard after connecting to the raspberry pi. We were able to init the CAN bus and  get the currents from each TalonSRX.

## Design Discussion

We will mostly be working on tasks in parallel. In order to do this effectively, we need to define the explicit API between each layer. Here is an example of what this API might look like between the C, Python, and Web layers. We need to make some design decisions in regard to what the outward facing API is for each layer before we start heavy implementation.

```yaml #
liblk: C library
	hardware:
		- Talon.cpp
			- set_power(float) -> void
			- get_current(void) -> float
			- get_ticks(void) -> float
		- Stepper.cpp
			- step(void) -> void
			- step_by(int) -> void
			- get_steps() -> int
		- IMU.cpp
			- get_heading() -> float
			- get_yaw() -> float
			- get_pitch() -> float
	robot:
		- Base.cpp
			- turn(float) -> void
			- travel(float) -> void
		- Intake.cpp
		- Depo.cpp
		- Robot.cpp
			- init(void) -> void
			- start_heartbeat() -> void
			- stop_all() -> void
	utils:
		- Logger.cpp

lkpy: Python C extension module
	- lkpymodule.cpp
		- create_robot(void) -> Robot
		- kill(void) -> boolean
		- get_status(void) -> Status

web api:
	POST:
		- /gamepad {input_id: value}
		- /kill
	GET:
		- /dashboard
		- /sensor?id=
```

## Preparing for Next Week

Besides thinking about some API design choices, here are some concepts you may want to look at in preparing for the implementation phase. Some of these resources will also help us make choices about the design.


### C/C++ Stuff

- [TalonSRX Library](https://github.com/CrossTheRoadElec/Phoenix-Linux-SocketCAN-Example/blob/master/include/ctre/phoenix/motorcontrol/can/TalonSRX.h)
- [Making Python extensions](https://docs.python.org/3/extending/extending.html)
- C Build Systems
	- [https://cmake.org/](https://cmake.org/)
	- [A bunch of methods](https://julienjorge.medium.com/an-overview-of-build-systems-mostly-for-c-projects-ac9931494444)

Some design choices to be made here are:

- What build system should we use?
- How should we structure the library?
- Object oriented or functional?

### Python Stuff

- Running C in Python
	- [FFI Concept](https://en.wikipedia.org/wiki/Foreign_function_interface)
	- [ctypes](https://docs.python.org/3/library/ctypes.html)
	- [cffi](https://cffi.readthedocs.io/en/latest/)
	- [C extensions](https://docs.python.org/3/extending/extending.html)
- [Type checking with mypy](https://mypy.readthedocs.io/en/stable/)

Some design choices to be made here are:

- What logic should be in Python instead of C?
- How should we load C libraries into Python?

### Web Stuff

- [Flask backend](https://flask.palletsprojects.com/en/2.0.x/)
- [Web sockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
	- [Flask sockets](https://flask-socketio.readthedocs.io/en/latest/)
	- [Js sockets](https://socket.io/)
- [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [POST & GET requests](https://www.w3schools.com/tags/ref_httpmethods.asp)

Some design choices to be made here are:

- What routes to have?
- What data should the sockets handle?


