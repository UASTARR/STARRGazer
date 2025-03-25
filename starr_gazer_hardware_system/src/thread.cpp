#include <exception>
#include <onnxruntime_cxx_api.h>
#include "camera.hpp"
#include "safequeue.hpp"

using Array = std::vector<float>;
using Shape = std::vector<long>;

std::pair<Array, Shape, cv::Mat> process_image(Ort::Session &session, Array &array, Shape shape, cv::Mat &frame)
{
    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);
    auto input = Ort::Value::CreateTensor<float>(
        memory_info, (float *)array.data(), array.size(), shape.data(), shape.size());

    const char *input_names[] = {"images"};
    const char *output_names[] = {"output"};
    auto output = session.Run(Ort::RunOptions{nullptr}, input_names, &input, 1, output_names, 1);

    shape = output[0].GetTensorTypeAndShapeInfo().GetShape();
    auto ptr = output[0].GetTensorData<float>();

    for (size_t i = 0; i < shape[0]; ++i)
    {
        int x = ptr[1], y = ptr[2], w = ptr[3] - x, h = ptr[4] - y, c = ptr[5];
        auto color = CV_RGB(255, 255, 255);
        std::string name = "Class" + std::to_string(c) + ":" + std::to_string(int(ptr[6] * 100)) + "%";
        cv::rectangle(frame, {x, y, w, h}, color);
        cv::putText(frame, name, {x, y}, cv::FONT_HERSHEY_DUPLEX, 1, color);
    }

    return {Array(ptr, ptr + shape[0] * shape[1]), shape, frame};
}

int main()
{
    std::cout << "Initializing Hardware System\n";
    std::cout << "Calibrating Gimbal\n";

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
    SafeQueue<std::tuple<Array, Shape, cv::Mat>> frameQueue;
    SafeQueue<std::pair<int, cv::Mat>> processedQueue;

    std::atomic<bool> processingDone(false);

    // Capture thread
    std::thread captureThread([&]()
                              {
        cv::Mat frame;
        while (!processingDone)
        {
            auto [array, shape, frame] = cam.getFrame();
            if (frame.empty())
            {
                break;
            }
            frameQueue.enqueue({array, shape, frame.clone()});
        }
        frameQueue.setFinished(); });

    // Processing thread
    std::thread processingThread([&]()
                                 {
        cv::Mat frame;
        Array array;
        Shape shape;
        while (!processingDone)
        {
            std::tuple<Array, Shape, cv::Mat> item;
            if (!frameQueue.dequeue(item))
                break;

            std::tie(array, shape, frame) = item;
            auto [output_array, output_shape, output_frame] = process_image(model, array, shape, frame);
            processedQueue.enqueue({processedQueue.size(), output_frame});
        }
        processedQueue.setFinished(); });

    // Writing thread
    std::thread writingThread([&]()
                              {
        std::pair<int, cv::Mat> processedFrame;
        while (!processingDone)
        {
            if (!processedQueue.dequeue(processedFrame))
                break;
            cam.writeFrame(processedFrame.second);
        } });

    // Main loop to check for exit condition
    while (!processingDone)
    {
        char c = (char)cv::waitKey(1);
        if (c == 27) // Esc key
        {
            processingDone = true;
        }
    }

    // Wait for all threads to finish
    captureThread.join();
    processingThread.join();
    writingThread.join();

    std::cout << "Video processing completed successfully." << std::endl;
    return 0;
}
