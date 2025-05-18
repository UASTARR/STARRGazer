#include "camera.hpp"
#include <thread>
#include <iostream>

<<<<<<< HEAD
=======
// GimbalCamera::GimbalCamera(int id, bool sendrtp)
// {
//     string source = "nvarguscamerasrc sensor-id=" + to_string(id) +
//                     " ! nvvidconv ! tee name=t ! ";
                    
//     source += "queue ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink t.";
//     if (sendrtp)
//     {
//         source += "queue ! x264enc bitrate=2000 speed-preset=ultrafast tune=zerolatency ! h264parse ! rtph264pay ! udpsink host=127.0.0.1 port=5000";
//     }


//     cap.open(source, cv::CAP_GSTREAMER);
//     cap.set(cv::CAP_PROP_CONVERT_RGB, true);
//     if (!cap.isOpened())
//     {
//         cerr << "Error: Unable to open camera" << endl;
//         exit(1);
//     }
//     // std::cout << cv::getBuildInformation() << std::endl;
//     vector<int> prop = getProp();
//     std::cout << "This is the properties: " << prop[0] << prop[1] << prop[2] << std::endl;
//     // writer.open("output.mp4", cv::VideoWriter::fourcc('M', 'P', '4', 'V'), prop[2], cv::Size(prop[0], prop[1]));
//     // if (!writer.isOpened())
//     // {
//     //     cerr << "Error: Unable to open video writer" << endl;
//     //     exit(1);
//     // }
// }
>>>>>>> e0d4a56 (Fixed bug: greyscale removed and not working RTP code)

GimbalCamera::GimbalCamera(int id, bool sendrtp)
{
    string source =
    "nvarguscamerasrc sensor-id=" + to_string(id) + " ! "
    "nvvidconv ! video/x-raw,format=NV12 ! tee name=t ! "
    
    // Branch 1: to OpenCV
    "queue ! nvvidconv ! video/x-raw,format=BGRx ! "
    "videoconvert ! video/x-raw,format=BGR ! appsink ";
    
    // Branch 2: to RTP stream
    // "t. ! queue ! nvvidconv ! video/x-raw,format=I420 ! "
    // "x264enc bitrate=2000 speed-preset=ultrafast tune=zerolatency ! "
    // "h264parse ! rtph264pay config-interval=1 pt=96 ! "
    // "udpsink host=127.0.0.1 port=5000";


    // // Conditional RTP streaming pipeline
    // // if (sendrtp)
    // // {
    // //     source += "queue ! nvv4l2h264enc maxperf-enable=1 insert-sps-pps=1 bitrate=2000000 "
    // //               " ! h264parse ! rtph264pay config-interval=1 pt=96 "
    // //               " ! udpsink host=127.0.0.1 port=5000 sync=false async=false";
    // // }

    // Initialize OpenCV capture
    cap.open(source, cv::CAP_GSTREAMER);
    cap.set(cv::CAP_PROP_CONVERT_RGB, true);
    if (!cap.isOpened())
    {
        cerr << "Error: Unable to open camera" << endl;
        exit(1);
    }

    // Get properties
    vector<int> prop = getProp();
    std::cout << "This is the properties: " << prop[0] << " " << prop[1] << " " << prop[2] << std::endl;
    int fourcc = VideoWriter::fourcc('M', 'P', '4', 'V');
    writer.open("output.mkv", fourcc, prop[2], Size(prop[0], prop[1]));
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

std::tuple<Array, Shape, cv::Mat> GimbalCamera::getFrame(std::tuple<int, int> size)
{
    Mat image;
    cap >> image;
    // std::cout << "Channels: " << image.channels() << std::endl;
    // std::cout << "Type: " << image.type() << std::endl;
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
