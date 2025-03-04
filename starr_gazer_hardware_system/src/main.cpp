#include <exception>
#include <opencv2/opencv.hpp>
#include <iostream>
#include "camera.hpp"

int main(void) {
  std::cout << "Initializing Hardware System\n";
  // TODO: Connect and Setup all Hardware Components (Inputs and Gimbal)
  std::cout << "Calibrating Gimbal\n";
  // TODO: Calibrate Gimbal
  std::cout << "Entering Event Loop\n";
  GimbalCamera cam(0);
  cv::Mat myImage;
  try {
    while (true) {
      myImage = cam.getFrame();
      if (myImage.empty()){ //Breaking the loop if no video frame is detected//
         break;
      }
      cv::imshow("Video Player", myImage);//Showing the video//
      char c = (char)cv::waitKey(25);//Allowing 25 milliseconds frame processing time and initiating break condition//
      if (c == 27){ //If 'Esc' is entered break the loop//
         break;
      }
    }
  } catch (const std::exception &e) {
    // TODO: use killswitch protocol if the program suddenly exits
    std::cerr << "Exiting Abnormally\n";
    return 1;
  }
  return 0;
}
