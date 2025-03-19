# Makefile for building GStreamer applications

# Compiler
CC = gcc

# Compiler flags
CFLAGS = `pkg-config --cflags --libs gstreamer-1.0`

# Source files
SRC_DIR = src
SRC_FILES = capture.c encoder.c filtered.c savecapture.c udpsinkwithh264.c

# Build directory
BUILD_DIR = build

# Object files
OBJ_FILES = $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRC_FILES))

# Default target
.DEFAULT_GOAL = $(BUILD_DIR)/capture

# Targets for each source file
$(BUILD_DIR)/capture: $(BUILD_DIR)/capture.o
	$(CC) -o $@ $^ $(CFLAGS)

$(BUILD_DIR)/encoder: $(BUILD_DIR)/encoder.o
	$(CC) -o $@ $^ $(CFLAGS)

$(BUILD_DIR)/filtered: $(BUILD_DIR)/filtered.o
	$(CC) -o $@ $^ $(CFLAGS)

$(BUILD_DIR)/savecapture: $(BUILD_DIR)/savecapture.o
	$(CC) -o $@ $^ $(CFLAGS)

$(BUILD_DIR)/udpsinkwithh264: $(BUILD_DIR)/udpsinkwithh264.o
	$(CC) -o $@ $^ $(CFLAGS)

# Target to build all
all: $(OBJ_FILES) $(BUILD_DIR)/capture $(BUILD_DIR)/encoder $(BUILD_DIR)/filtered $(BUILD_DIR)/savecapture $(BUILD_DIR)/udpsinkwithh264

# Pattern rule for building object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(BUILD_DIR)
	$(CC) -c $< -o $@ $(CFLAGS)

# Clean target
clean:
	rm -rf $(BUILD_DIR)/*.o $(BUILD_DIR)/*

.PHONY: all clean

