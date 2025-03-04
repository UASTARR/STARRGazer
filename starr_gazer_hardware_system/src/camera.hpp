#pragma once
#include<opencv2/opencv.hpp>


int displayCamera();

class GimbalCamera {
    public:
    GimbalCamera(int id);
    ~GimbalCamera();
    cv::Mat getFrame();
    private:
    cv::VideoCapture cap;
};