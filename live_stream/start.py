# stream_to_rtmp.py
import subprocess

STREAM_URL = "rtmp://localhost/live/stream1"
# Use v4l2 for webcam input
WEBCAM_FORMAT = "v4l2"
WEBCAM_SOURCE = "/dev/video0"

def start_stream():
    """
    Start the webcam stream using ffmpeg and send it to the RTMP server.
    """
    source = int(input("Enter the source (1 for webcam, 2 for file): "))
    source = 2
    if source == 1:
        # Webcam stream
        cmd = [
            "ffmpeg",
            "-f", WEBCAM_FORMAT,
            "-i", WEBCAM_SOURCE,
            "-f", "flv",
            STREAM_URL
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