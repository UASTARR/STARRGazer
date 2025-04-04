TARGET := hardware_system
SRC_DIR := src
BUILD_DIR := build

CXX := g++
CXXFLAGS := -std=c++17 -Wall   $(shell pkg-config --cflags opencv4 libonnxruntime) -I3rdParty/CppGPIO/include -I3rdParty/spidev-lib/src 
LDFLAGS := $(shell pkg-config --libs opencv4 libonnxruntime) -L3rdParty/CppGPIO -l:libcppgpio.a -L3rdParty/spidev-lib -l:libspidev.a


.PHONY: all clean
all: $(BUILD_DIR)/$(TARGET)

clean:
	rm -r build/*
	rm 3rdParty/spidev-lib/libspidev.a
	make -C 3rdParty/CppGPIO clean

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/$(TARGET): $(BUILD_DIR)/main.o  $(BUILD_DIR)/camera.o | 3rdParty/CppGPIO/libcppgpio.a 3rdParty/spidev-lib/libspidev.a
	$(CXX) $^ $(LDFLAGS) -o $@  

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.cpp | $(SRC_DIR)/camera.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(SRC_DIR)/%.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

# Dependencies
3rdParty/CppGPIO/libcppgpio.a:
	make -C 3rdParty/CppGPIO

3rdParty/spidev-lib/libspidev.a:
	$(CC) -std=c++14 -Wall -Werror -Wpedantic -o 3rdParty/spidev-lib/libspidev.a -c 3rdParty/spidev-lib/src/spidev_lib++.cc
