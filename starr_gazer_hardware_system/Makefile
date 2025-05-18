TARGET := hardware_system
SRC_DIR := src
BUILD_DIR := build

CXX := g++
CXXFLAGS := -std=c++17 -Wall -I/usr/include/opencv4 -I3rdParty/onnxruntime/include -I3rdParty/CppGPIO/include -I3rdParty/spidev-lib/include
# -L3rdParty/onnxruntime/lib -lonnxruntime  for onnx
LDFLAGS := -lopencv_gapi -lopencv_highgui -lopencv_ml -lopencv_objdetect -lopencv_photo -lopencv_stitching -lopencv_video -lopencv_calib3d -lopencv_features2d -lopencv_dnn -lopencv_flann -lopencv_videoio -lopencv_imgcodecs -lopencv_imgproc -lopencv_core -L3rdParty/CppGPIO -l:libcppgpio.a -L3rdParty/spidev-lib/lib -l:libspidev.a


.PHONY: all clean
all: $(BUILD_DIR)/$(TARGET)

motor: $(BUILD_DIR)/motor_test

camera_test: $(BUILD_DIR)/camera_test

$(BUILD_DIR)/motor_test: $(BUILD_DIR)/motor.o $(BUILD_DIR)/motor_test.o
	$(CXX) $^ $(LDFLAGS) -o $@  

$(BUILD_DIR)/motor_test.o: $(SRC_DIR)/motor_test.cpp | $(SRC_DIR)/motor.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

$(BUILD_DIR)/motor.o: $(SRC_DIR)/motor.cpp | $(SRC_DIR)/motor.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

$(BUILD_DIR)/camera_test: $(BUILD_DIR)/camera.o $(BUILD_DIR)/camera_test.o
	$(CXX) $^ $(LDFLAGS) -o $@  

$(BUILD_DIR)/camera_test.o: $(SRC_DIR)/camera_test.cpp | $(SRC_DIR)/camera.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

$(BUILD_DIR)/camera.o: $(SRC_DIR)/camera.cpp | $(SRC_DIR)/camera.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 	
	
clean:
	rm -r build/*
	# make -C 3rdParty/spidev-lib clean
	# make -C 3rdParty/CppGPIO clean

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/$(TARGET): $(BUILD_DIR)/main.o  $(BUILD_DIR)/camera.o | 3rdParty/CppGPIO/libcppgpio.a 3rdParty/spidev-lib/lib/libspidev.a
	$(CXX) $^ $(LDFLAGS) -o $@  

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.cpp | $(SRC_DIR)/camera.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(SRC_DIR)/%.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

# Dependencies
3rdParty/CppGPIO/libcppgpio.a:
	make -C 3rdParty/CppGPIO

3rdParty/spidev-lib/lib/libspidev.a:
	make -C 3rdParty/spidev-lib
