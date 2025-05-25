#include <cppgpio.hpp>
#include "motor.hpp"

GimbalMotor::GimbalMotor(int stepPin, int dirPin, int enablePin)
    : gimbalStepPin(stepPin, 1024, 0), gimbalDirPin(dirPin), gimbalEnablePin(enablePin) {
}

GimbalMotor::~GimbalMotor() {}

void GimbalMotor::enable() {
  gimbalEnablePin.on();
}

void GimbalMotor::disable() {
  gimbalEnablePin.off(); 
}

void GimbalMotor::setDirection(GimbalMotorDirection dir) {
  if (dir == LEFT) {
    gimbalDirPin.on();
  }
  else {
    gimbalDirPin.off();
  }
}

void GimbalMotor::step() {
  gimbalStepPin.set_ratio(100);
  // TODO: sleep
  gimbalStepPin.set_ratio(0);
}

void GimbalMotor::setRatio(int ratio) {
  gimbalStepPin.set_ratio(ratio);
}

void GimbalMotor::turn(int angle) {
  // TODO: do the math to calculate how many steps to do 
  // TODO: do the math to calculate how fast and long i should enable pwm for
}
