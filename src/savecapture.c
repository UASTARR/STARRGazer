#include <gst/gst.h>
#include <glib.h>
#include <signal.h>

GMainLoop *loop;
GstElement *pipeline;

/* Signal handler to catch Ctrl+C and stop the pipeline safely */
void handle_signal(int signum) {
    g_print("\nCaught signal %d, stopping pipeline...\n", signum);
    if (pipeline) {
        gst_element_send_event(pipeline, gst_event_new_eos());  // Send EOS event
    }
}

int main(int argc, char *argv[]) {
    GstElement *source, *convert, *sink;
    GstBus *bus;
    GstMessage *msg;
    GstStateChangeReturn ret;

    /* Initialize GStreamer */
    gst_init(&argc, &argv);
    loop = g_main_loop_new(NULL, FALSE);

    /* Create elements */
    source = gst_element_factory_make("nvarguscamerasrc", "source");
    convert = gst_element_factory_make("nvvidconv", "convert");
    sink = gst_element_factory_make("filesink", "sink");

    /* Create the pipeline */
    pipeline = gst_pipeline_new("camera-pipeline");

    if (!pipeline || !source || !convert || !sink) {
        g_printerr("Not all elements could be created.\n");
        return -1;
    }

    /* Set properties */
    g_object_set(source, "sensor-id", 0, NULL);
    g_object_set(sink, "location", "output.raw", NULL);

    /* Build the pipeline */
    gst_bin_add_many(GST_BIN(pipeline), source, convert, sink, NULL);
    if (!gst_element_link_many(source, convert, sink, NULL)) {
        g_printerr("Elements could not be linked.\n");
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
    g_print("Recording... Press Ctrl+C to stop.\n");
    g_main_loop_run(loop);  // Keeps pipeline running

    /* Stop the pipeline on EOS */
    g_print("Stopping pipeline...\n");
    gst_element_set_state(pipeline, GST_STATE_NULL);

    /* Free resources */
    gst_object_unref(pipeline);
    g_main_loop_unref(loop);
    return 0;
}
