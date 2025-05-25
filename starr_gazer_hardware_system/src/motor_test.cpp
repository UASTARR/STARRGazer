#include <chrono>
#include "motor.hpp" 
#include <iostream>

#define POWER 50

int main(void) {
	std::cout << "Starting the motor\n";
	GimbalMotor motor(33, 32, 23);
	motor.setRatio(POWER);
	std::cout << "The motor is running\n";
	std::this_thread::sleep_for(std::chrono::milliseconds(100));
	motor.setRatio(0);
	std::cout << "The motor has stopped\n";
	return 0;
}
