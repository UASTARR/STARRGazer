#pragma once

#include <cppgpio.hpp>

// This step angle will be confirmed once I talk to avionics - Sovereign
#define STEP_ANGLE 1

enum GimbalMotorDirection {
  LEFT,
  RIGHT
};

class GimbalMotor {
public:
  GimbalMotor(int stepPin, int dirPin, int enablePin);
  ~GimbalMotor();
  void enable();
  void disable();
  void setDirection(GimbalMotorDirection dir);
  void step();
  void turn(int angle);

private:
  GPIO::PWMOut gimbalStepPin;
  GPIO::DigitalOut gimbalDirPin, gimbalEnablePin;
};
