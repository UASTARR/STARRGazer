#include <exception>

#include "camera.hpp"
#include "third_party/YOLO11Seg.hpp"

int main(void)
{
  std::cout << "Initializing Hardware System\n";
  // TODO: Connect and Setup all Hardware Components (Inputs and Gimbal)

  std::cout << "Calibrating Gimbal\n";
  // TODO: Calibrate Gimbal

  std::cout << "Loading the model\n";
  const std::string labelsPath = "../models/coco.names";      // Path to class labels
  const std::string modelPath = "../models/yolo11n-seg.onnx"; // Path to model
  const bool isGPU = true;
  YOLOv11SegDetector segmentor(modelPath, labelsPath, isGPU);

  std::cout << "Entering Event Loop\n";
  GimbalCamera cam(0);
  cv::Mat frame;
  try
  {
    while (true)
    {
      // Get the image
      frame = cam.getFrame();
      if (myImage.empty())
      { // Breaking the loop if no video frame is detected//
        break;
      }

      // Process the image
      std::vector<Detection> results = segmentor.detect(frame);
      detector.drawBoundingBoxMask(frame, results);

      // Show the image
      cv::imshow("Video Player", frame); // Showing the video//

      // Save the image
      cam.writeFrame(frame);

      char c = (char)cv::waitKey(25); // Allowing 25 milliseconds frame processing time and initiating break condition//
      if (c == 27)
      { // If 'Esc' is entered break the loop//
        break;
      }
    }
  }
  catch (const std::exception &e)
  {
    // TODO: use killswitch protocol if the program suddenly exits
    std::cerr << "Exiting Abnormally\n";
    return 1;
  }
  return 0;
}
