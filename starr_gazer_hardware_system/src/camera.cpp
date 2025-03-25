#include "camera.hpp"

GimbalCamera::GimbalCamera(int id)
{
    string source = "nvarguscamerasrc sensor-id=" + to_string(id) +
                    " ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink";
    cap.open(source, cv::CAP_GSTREAMER);
    cap.set(cv::CAP_PROP_CONVERT_RGB, true);
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

std::tuple<Array, Shape, cv::Mat> GimbalCamera::getFrame(std::tuple<int, int> size = {1920, 1080})
{
    Mat image;
    cap >> image;
    std::cout << "Channels: " << frame.channels() << std::endl;
    std::cout << "Type: " << frame.type() << std::endl;
    assert(!image.empty() && image.channels() == 3);
    cv::resize(image, image, {get<0>(size), get<1>(size)});
    Shape shape = {1, image.channels(), image.rows, image.cols};
    cv::Mat nchw = cv::dnn::blobFromImage(image, 1.0, {}, {}, true) / 255.f;
    Array array(nchw.ptr<float>(), nchw.ptr<float>() + nchw.total());
    return {array, shape, image};
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
