#pragma once

#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <tuple>

using namespace std;
using namespace cv;
using Array = std::vector<float>;
using Shape = std::vector<long>;

int displayCamera();

class GimbalCamera
{
public:
    GimbalCamera(int id, bool sendrtp);

    ~GimbalCamera();
    std::tuple<Array, Shape, cv::Mat> getFrame(std::tuple<int, int> size = std::make_tuple(1920, 1080));
        vector<int> getProp();
    void writeFrame(Mat frame);

private:
    VideoCapture cap;
    VideoWriter writer;
    int fourcc;
};
