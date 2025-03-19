#include "camera.hpp"

GimbalCamera::GimbalCamera(int id)
{
    string source = "nvarguscamerasrc sensor-id=" + to_string(id) + " ! nvvidconv ! appsink";
    cap.open(source, cv::CAP_GSTREAMER);
    if (!cap.isOpened())
    {
        cerr << "Error: Unable to open camera" << endl;
        exit(1);
    }
    vector<int> prop = getProp();
    writer.open("output", cv::VideoWriter::fourcc('M', 'P', '4', 'V'), prop[2], cv::Size(prop[0], prop[1]));
    if (!writer.isOpened())
    {
        cerr << "Error: Unable to open video writer" << endl;
        exit(1);
    }
}

GimbalCamera::~GimbalCamera()
{
    cap.release();
    writer.release();
    cv::destroyAllWindows();
}

Mat GimbalCamera::getFrame()
{
    Mat currentFrame;
    cap >> currentFrame;
    return currentFrame;
}

vector<int> GimbalCamera::getProp()
{
    vector<int> prop;
    prop.push_back(static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH)));
    prop.push_back(static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT)));
    prop.push_back(static_cast<int>(cap.get(cv::CAP_PROP_FPS)));
    return prop;
}

void GimbalCamera::writeFrame(Mat frame)
{
    writer.write(frame);
}
