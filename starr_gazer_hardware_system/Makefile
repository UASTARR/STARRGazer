TARGET := hardware_system
SRC_DIR := src
BUILD_DIR := build

CXX := g++
CXXFLAGS := -Wall -Werror -Wpedantic  $(shell pkg-config --cflags opencv4)
LDFLAGS := $(shell pkg-config --libs opencv4)

.PHONY: all clean
all: $(BUILD_DIR)/$(TARGET)

clean:
	rm -r build/*

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/$(TARGET): $(BUILD_DIR)/main.o  $(BUILD_DIR)/camera.o 
	$(CXX) $^ $(LDFLAGS) -o $@  

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.cpp | $(SRC_DIR)/camera.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(SRC_DIR)/%.hpp $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $< 

