# Introduction

pwmStepper implements a bipolar stepper motor driver for the Raspberry Pi Pico (RASP2). The board must be connected to a hardware driver which can be either DRV8834 or MPU6500 from Pololu.

The driver takes benefit of the RASP2 PIO feature to generate a pwm with acurate period to drive the step pin. The pulse width is set to 3 microseconds.

The step resolution and motor speed can be set and changed 'on the flight'.

Two motors can be driven simultaneoulsy.

# The wiring

![wiring](wiring.png)

# The driver

Copy pwmStepper.py in the RASP2 filesystem, then:

    >>> from pwmStepper import pwmStep
    >>> m0 = pwmStep(0)      # instantiate motor 0 with default config
    >>> m1 = pwmStep(1)      # instantiate motor 1 with default config
    >>> m0.doSteps(100)      # move motor 0 100 steps forward
    >>> m2.doSteps(-50)      # move motor 1 50 steps backward

## Configuration parameters

They must be set at object creation time:

    >>> m0 = pwmStep(..., param=param_value, ...)

with *param* being:

- __dev__ (string) : the hardware motor driver. At present, only two devices implemented: 'DRV8834' and 'MPU6500'. Default is 'DRV8834'.
- __step_size__ (float) : the stepper full step size, in user units (eg 1.8 for a Nema 200 steps/rotation)
- __step_unit__ (string) : the step unit (eg 'deg', 'mm')
- __stepRes__ (int) : initial step resolution (1=full step, 2=half step, 4=quarter step, ...). Default is 1.
- __max_speed__ (float) : the maximum rotation speed, in steep_unit/s
- __min_speed__ (float) : the minimum rotation speed, in steep_unit/s

