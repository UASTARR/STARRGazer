#pragma once

#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

int displayCamera();

class GimbalCamera
{
public:
    GimbalCamera(int id);
    ~GimbalCamera();
    std::tuple<Array, Shape, cv::Mat> getFrame(std::tuple<int, int> size = {1920, 1080});
        vector<int> getProp();
    void writeFrame(Mat frame);

private:
    VideoCapture cap;
    VideoWriter writer;
};