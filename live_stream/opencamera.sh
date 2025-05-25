gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! nvvidconv ! queue ! avenc_mpeg4 ! queue ! mpeg4videoparse ! queue ! nvv4l2decoder ! queue ! nv3dsink -e

