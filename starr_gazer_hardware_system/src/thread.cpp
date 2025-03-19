#include <exception>

#include "camera.hpp"
#include "third_party/YOLO11Seg.hpp"
#include "third_party/safequeue.hpp"

int main()
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

    // Thread-safe queues and processing...
    // Thread-safe queues
    SafeQueue<cv::Mat> frameQueue;
    SafeQueue<std::pair<int, cv::Mat>> processedQueue;

    // Flag to indicate processing completion
    std::atomic<bool> processingDone(false);

    // Capture thread
    std::thread captureThread([&]()
                              {
        cv::Mat frame;
        int frameCount = 0;
        while (!processingDone)
        {
            frame = cam.getFrame();
            if (frame.empty())
            {
                break;
            }
            frameQueue.enqueue(frame.clone()); // Clone to ensure thread safety
            frameCount++;
        }
        frameQueue.setFinished(); });

    // Processing thread
    std::thread processingThread([&]()
                                 {
        cv::Mat frame;
        int frameIndex = 0;
        while (frameQueue.dequeue(frame) && !processingDone)
        {
            // Detect objects in the frame
            std::vector<Detection> results = detector.detect(frame);

            // Draw bounding boxes on the frame
            detector.drawBoundingBoxMask(frame, results); // Uncomment for mask drawing

            // Enqueue the processed frame
            processedQueue.enqueue(std::make_pair(frameIndex++, frame));
        }
        processedQueue.setFinished(); });

    // Writing thread
    std::thread writingThread([&]()
                              {
        std::pair<int, cv::Mat> processedFrame;
        while (processedQueue.dequeue(processedFrame) && !processingDone)
        {
            cam.writeFrame(processedFrame.second);
        } });

    // Release resources
    char c = (char)if (c == 27)
    { // If 'Esc' is entered break the loop//
        processingDone = true;
    }

    // Wait for all threads to finish
    captureThread.join();
    processingThread.join();
    writingThread.join();

    std::cout << "Video processing completed successfully." << std::endl;

    return 0;
}