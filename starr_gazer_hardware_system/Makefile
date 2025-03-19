TARGET := hardware_system
SRC_DIR := src
BUILD_DIR := build

CXX := g++
CXXFLAGS := -Wall -Werror -Wpedantic  $(shell pkg-config --cflags opencv4)
LDFLAGS := $(shell pkg-config --libs opencv4)

MAIN := $(SRC_DIR)/main.cpp

.PHONY: all clean
all: $(BUILD_DIR)/$(TARGET)

clean:
	rm -r build/*

init:
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/$(TARGET): $(BUILD_DIR)/main.o $(BUILD_DIR)/camera.o 
	$(CXX) $^ $(LDFLAGS) -o $@  

$(BUILD_DIR)/main.o: $(SRC_DIR)/${MAIN} $(SRC_DIR)/camera.hpp
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

$(BUILD_DIR)/camera.o: $(SRC_DIR)/camera.cpp $(SRC_DIR)/camera.hpp
	$(CXX) $(CXXFLAGS) -o $@ -c $<