# stream_to_rtmp.py
import subprocess

STREAM_URL = "rtmp://localhost/live/camera0"
# Use v4l2 for webcam input
WEBCAM_FORMAT = "v4l2"
WEBCAM_SOURCE = "/dev/video1"

def start_stream():
    """
    Start the webcam stream using gstreamer and send it to the RTMP server.
    """
    source = int(input("Enter the source (1 for webcam, 2 for file): "))
    if source == 1:
        # Webcam stream
        # cmd = [
        #     "ffmpeg",
        #     "-rtsp_transport", "tcp"
        #     "-f", WEBCAM_FORMAT,
        #     "-i", WEBCAM_SOURCE,
        #     "-c:v", "libx264",
        #     "-f", "flv",
        #     STREAM_URL
        # ]
        # cmd = [
        #     "gst-launch-1.0",
        #     "nvarguscamerasrc", "sensor-id=0",
        #     "!", "nvvidconv",
        #     # "!", "queue",  # Add queue element
        #     "!", "x264enc",
        #     # "!", "queue",  # Add queue element
        #     "!", "flvmux",
        #     # "!", "queue",  # Add queue element
        #     "!", "rtmpsink", f"location={STREAM_URL}"
        # ]
        cmd = [
            "gst-launch-1.0",
            "nvarguscamerasrc", "sensor-id=0",
            # "!", "video/x-raw(memory:NVMM),width=1920,height=1080,framerate=60/1",
            "!", "nvvidconv",
            # "!", "video/x-raw,format=I420"
            "!", "queue",       # Add queue
            "!", "x264enc", "bitrate=2000", "speed-preset=ultrafast", "tune=zerolatency",
            # "!", "flvmux", "streamable=true",
            "!", "rtph264pay",
            "!", "udpsink", "host=127.0.0.1", "port=5000", "auto-multicast=true"
            # "!", "rtmpsink", f"location={STREAM_URL}"
            # "!", "hlssink", "location=/var/www/html/hls/hlssink.%05d.ts", "playlist-location=/var/www/html/hls/stream1.m3u8", "target-duration=1"
        ]
    elif source == 2:
        # File stream
        file_path = input("Enter the file path: ")
        cmd = [
            "ffmpeg",
            "-re",
            # "-stream_loop", "-1",
            "-i", file_path,
            "-c", "copy",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-f", "flv",
            "-flvflags", "no_duration_filesize",
            STREAM_URL
        ]
    else:
        print("Invalid source selected.")
        return
    
    subprocess.run(cmd)

start_stream()