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
    Mat getFrame();
    vector<int> getProp();
    void writeFrame(Mat frame);

private:
    VideoCapture cap;
    VideoWriter writer;
};