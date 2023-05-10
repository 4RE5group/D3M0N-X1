keyboard_MOD_DIR := $(USERMOD_DIR)

# Add our source files to the respective variables.
SRC_USERMOD += $(keyboard_MOD_DIR)/keyboard.c
SRC_USERMOD_CXX += $(keyboard_MOD_DIR)/keyboard.cpp

# Add our module directory to the include path.
CFLAGS_USERMOD += -I$(keyboard_MOD_DIR)
CXXFLAGS_USERMOD += -I$(keyboard_MOD_DIR) -std=c++11

# We use C++ features so have to link against the standard library.
LDFLAGS_USERMOD += -lstdc++