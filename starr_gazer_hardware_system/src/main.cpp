#include <exception>
#include "camera.hpp"
#include <onnxruntime_cxx_api.h>

using Array = std::vector<float>;
using Shape = std::vector<long>;

/*
 * This code was inspired by an implementation from:
 * Source: https://medium.com/@shahriar.rezghi.sh/using-yolo-in-c-55d55419a947
 * Author: Shahriar Rezghi
 */

std::pair<Array, Shape, cv::Mat> process_image(Ort::Session &session, Array &array, Shape shape, cv::Mat &frame)
{
  auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);
  auto input = Ort::Value::CreateTensor<float>(
      memory_info, array.data(), array.size(), shape.data(), shape.size());

  const char *input_names[] = {"images"};  // Dont understand this
  const char *output_names[] = {"output"}; // Dont understand this
  auto output = session.Run(Ort::RunOptions{nullptr}, input_names, &input, 1, output_names, 1);

  shape = output[0].GetTensorTypeAndShapeInfo().GetShape();
  auto ptr = output[0].GetTensorData<float>();
  Array output_array(ptr, ptr + shape[0] * shape[1]);

  for (size_t i = 0; i < shape[0]; ++i)
  {
    auto data = output_array.data() + i * shape[1];
    int x = data[1], y = data[2], w = data[3] - x, h = data[4] - y, c = data[5];

    auto color = CV_RGB(255, 255, 255);
    std::string name = "Class" + std::to_string(c) + ":" + std::to_string(int(data[6] * 100)) + "%";
    cv::rectangle(frame, {x, y, w, h}, color);
    cv::putText(frame, name, {x, y}, cv::FONT_HERSHEY_DUPLEX, 1, color);
  }

  return {Array(ptr, ptr + shape[0] * shape[1]), shape, frame};
}

int main()
{
  std::cout << "Initializing Hardware System\n";
  // TODO: Connect and Setup all Hardware Components (Inputs and Gimbal)

  std::cout << "Calibrating Gimbal\n";
  // TODO: Calibrate Gimbal

  std::cout << "Loading the model\n";
  bool use_cuda = true;
  std::string model_path = "../model/YOLOv11.onnx";

  Ort::Env env(OrtLoggingLevel::ORT_LOGGING_LEVEL_WARNING, "YOLOv11");
  Ort::SessionOptions sessionOptions;
  sessionOptions.SetIntraOpNumThreads(1);
  if (use_cuda)
  {
    Ort::ThrowOnError(OrtSessionOptionsAppendExecutionProvider_CUDA(sessionOptions, 0));
  }
  Ort::Session model(env, model_path.c_str(), sessionOptions);

  std::cout << "Entering Event Loop\n";
  GimbalCamera cam(0);
  cv::Mat frame;

  try
  {
    while (true)
    {
      // Get the image
      auto [array, shape, frame] = cam.getFrame();
      if (frame.empty())
      {
        std::cerr << "Warning: Empty frame received.\n";
        continue;
      }

      // Process the image
      auto [array_out, shape_out, output] = process_image(model, array, shape, frame);

      // Show the image
      cv::imshow("Video Player", output);

      // Save the image
      cam.writeFrame(output);

      // Check for exit condition (Esc key)
      char c = (char)cv::waitKey(25);
      if (c == 27)
      {
        std::cout << "Exiting...\n";
        break;
      }
    }
  }
  catch (const std::exception &e)
  {
    std::cerr << "Exiting Abnormally: " << e.what() << "\n";
    return 1;
  }

  return 0;
}
