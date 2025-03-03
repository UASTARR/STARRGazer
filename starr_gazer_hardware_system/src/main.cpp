#include <exception>
#include <iostream>

int main(void) {
  std::cout << "Initializing Hardware System\n";
  // TODO: Connect and Setup all Hardware Components (Inputs and Gimbal)
  std::cout << "Calibrating Gimbal\n";
  // TODO: Calibrate Gimbal
  std::cout << "Entering Event Loop\n";
  try {
    while (true) {
    }
  } catch (const std::exception &e) {
    // TODO: use killswitch protocol if the program suddenly exits
    std::cerr << "Exiting Abnormally\n";
    return 1;
  }
  return 0;
}
