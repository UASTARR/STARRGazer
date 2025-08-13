# Creates a dummy webcam device and feeds the camera stream to it
sudo modprobe v4l2loopback
v4l2-ctl --list-devices
pkill gphoto2
# Starts the feeding camera to dummy webcam
gphoto2 --stdout --capture-movie | ffmpeg -loglevel verbose -i - -vcodec rawvideo -pix_fmt yuv420p -f v4l2 /dev/video0

# Comment out above and Uncomment the following to save video at the same time
# gphoto2 --stdout --capture-movie | ffmpeg -loglevel verbose -i - -vcodec rawvideo -pix_fmt yuv420p -f v4l2 /dev/video0 \
# -c:v libx264 -preset ultrafast -crf 18 "saved_videos/$(date +%Y%m%d_%H%M%S).mkv"