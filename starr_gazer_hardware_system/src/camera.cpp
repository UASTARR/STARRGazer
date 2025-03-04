#include <opencv2/opencv.hpp>//OpenCV header to use VideoCapture class//
#include <iostream>
#include <string>
#include "camera.hpp"


GimbalCamera::GimbalCamera(int id) {
    std::string source = "nvarguscamerasrc sensor-id=" + std::to_string(id) + " ! nvvidconv ! appsink";
    cap.open(source, cv::CAP_GSTREAMER);
}

GimbalCamera::~GimbalCamera() {
    cap.release();
}

cv::Mat GimbalCamera::getFrame() {
    cv::Mat currentFrame;
    cap >> currentFrame;
    return currentFrame;
}