TARGET := hardware_system
SRC_DIR := src
BUILD_DIR := build

CXX := g++
CXXFLAGS := -Wall -Werror -Wpedantic
LDFLAGS :=

.PHONY: all
all: $(BUILD_DIR)/$(TARGET)

init:
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/$(TARGET): $(BUILD_DIR)/main.o 
	$(CXX) $(LDFLAGS) $? -o $@

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.cpp 
	$(CXX) $(CXXFLAGS) -o $@ -c $? 

