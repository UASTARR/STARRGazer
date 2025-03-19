#include <gst/gst.h>
#include <glib.h>
#include <signal.h>

GMainLoop *loop;
GstElement *pipeline;

/*
gst-launch-1.0 nvarguscamerasrc ! nvvidconv ! nvv4l2h264enc ! tee name=t t. ! queue ! rtph264pay ! udpsink host=127.0.0.1 port=8001 t. ! queue ! h264parse ! qtmux ! filesink location=newtest.mp4

gst-launch-1.0 udpsrc address=127.0.0.1 port=8001 caps='application/x-rtp, encoding-name=H264, payload=96' ! rtph264depay ! queue ! h264parse ! nvv4l2decoder ! nv3dsink -e

*/
/* Signal handler to catch Ctrl+C and stop the pipeline safely */
void handle_signal(int signum) {
    g_print("\nCaught signal %d, stopping pipeline...\n", signum);
    if (pipeline) {
        gst_element_send_event(pipeline, gst_event_new_eos());  // Send EOS event
    }
}

int main(int argc, char *argv[]) {
    GstElement *source, *convert, *encoder, *parser, *tee, *queue1, *queue2, *muxer, *sink, *decoder, *vissink, *rtppay, *udpsink;
    GstBus *bus;
    GstMessage *msg;
    GstStateChangeReturn ret;

    /* Initialize GStreamer */
    gst_init(&argc, &argv);
    loop = g_main_loop_new(NULL, FALSE);

    /* Create elements */
    source = gst_element_factory_make("nvarguscamerasrc", "source");
    convert = gst_element_factory_make("nvvidconv", "convert");
    encoder = gst_element_factory_make("nvv4l2h264enc", "encoder");
    parser = gst_element_factory_make("h264parse", "parser");
    tee = gst_element_factory_make("tee", "tee");
    queue1 = gst_element_factory_make("queue", "queue1");
    queue2 = gst_element_factory_make("queue", "queue2");
    rtppay = gst_element_factory_make("rtph264pay", "rtppay");
    udpsink = gst_element_factory_make("udpsink", "udpsink");
    muxer = gst_element_factory_make("qtmux", "muxer");
    sink = gst_element_factory_make("filesink", "sink");
    decoder = gst_element_factory_make("nvv4l2decoder", "decoder");
    vissink = gst_element_factory_make("nv3dsink", "vissink");

    /* Create the pipeline */
    pipeline = gst_pipeline_new("camera-pipeline");

    if (!pipeline || !source || !convert || !encoder || !tee || !queue1 || !rtppay || !udpsink || !queue2 || !parser || !muxer || !sink) {
        g_printerr("Not all elements could be created.\n");
        return -1;
    }

    /* Set properties */
    g_object_set(source, "sensor-id", 0, NULL);
    g_object_set(sink, "location", "26-2-2025-6-00-h264.mp4", NULL);
    g_object_set(udpsink, "host", "127.0.0.1", "port", 8001, NULL);
    // g_object_set(rtppay, "mtu", 1400, "config-interval", 1, "pt", 96, NULL);

    /* Build the pipeline */
    gst_bin_add_many(GST_BIN(pipeline), source, convert, encoder, tee, queue1, rtppay, udpsink, queue2, parser, muxer, sink, NULL);
    if (!gst_element_link_many(source, convert, encoder, tee, NULL) ||
        !gst_element_link_many(queue1, rtppay, udpsink, NULL) ||
        !gst_element_link_many(queue2, parser, muxer, sink, NULL))
    {
        g_printerr("Elements could not be linked.\n");
        gst_object_unref(pipeline);
        return -1;
    }

    /* Manually link the tee to both branches */
    if (!gst_element_link(tee, queue1) || !gst_element_link(tee, queue2)){
        g_printerr("Tee element could not be linked properly\n");
        gst_object_unref(pipeline);
        return -1;
    }

    /* Catch termination signals */
    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);

    /* Start playing */
    ret = gst_element_set_state(pipeline, GST_STATE_PLAYING);
    if (ret == GST_STATE_CHANGE_FAILURE) {
        g_printerr("Unable to set the pipeline to the playing state.\n");
        gst_object_unref(pipeline);
        return -1;
    }

    /* Run the main loop */
    g_print("Streaming and Recording... Press Ctrl+C to stop.\n");
    g_main_loop_run(loop);  // Keeps pipeline running

    /* Stop the pipeline on EOS */
    g_print("Stopping pipeline...\n");
    gst_element_set_state(pipeline, GST_STATE_NULL);

    /* Free resources */
    gst_object_unref(pipeline);
    g_main_loop_unref(loop);
    return 0;
}
