#include "camera.hpp"

int main()
{
  GimbalCamera cam(0, true);
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
      cv::imshow("Video Player", frame);
      cam.writeFrame(frame);
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
